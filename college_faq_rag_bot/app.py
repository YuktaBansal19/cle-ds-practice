import os
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from pypdf import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from google import genai

load_dotenv()

st.set_page_config(page_title="College FAQ Bot", page_icon="🎓")
st.title("🎓 College FAQ Bot")
st.caption("Ask questions about a college handbook, syllabus, or other documents.")

API_KEY = os.getenv("GEMINI_API_KEY", "").strip()

def read_uploaded_file(uploaded_file):
    """Extract text from a PDF or plain-text file."""
    name = uploaded_file.name.lower()
    if name.endswith(".pdf"):
        reader = PdfReader(uploaded_file)
        pages = []
        for page in reader.pages:
            pages.append(page.extract_text() or "")
        return "\n".join(pages)
    return uploaded_file.getvalue().decode("utf-8", errors="ignore")

def split_into_chunks(text, chunk_size=900, overlap=150):
    """Split document text into overlapping chunks."""
    text = " ".join(text.split())
    if not text:
        return []
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append(text[start:end])
        if end == len(text):
            break
        start = end - overlap
    return chunks

def retrieve_chunks(question, chunks, vectorizer, chunk_vectors, top_k=4):
    question_vector = vectorizer.transform([question])
    scores = cosine_similarity(question_vector, chunk_vectors).flatten()
    best_indices = scores.argsort()[::-1][:top_k]
    return [(chunks[i], float(scores[i])) for i in best_indices if scores[i] > 0]

def answer_with_gemini(question, retrieved, client):
    context = "\n\n".join(
        f"[Source {i + 1}]\n{chunk}" for i, (chunk, _) in enumerate(retrieved)
    )
    prompt = f"""
You are a helpful college FAQ assistant.
Answer the student's question using ONLY the context below.
If the context does not contain the answer, say:
"I couldn't find that information in the uploaded documents."
Do not invent college policies, dates, fees, or requirements.
Keep the answer clear and concise.

CONTEXT:
{context}

STUDENT QUESTION:
{question}
"""
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )
    return response.text or "I couldn't generate an answer. Please try again."

with st.sidebar:
    st.header("1. Add documents")
    uploaded_files = st.file_uploader(
        "Upload college documents (PDF, TXT)",
        type=["pdf", "txt"],
        accept_multiple_files=True,
    )
    st.caption("Tip: Start with a syllabus, student handbook, or FAQ document.")
    st.divider()
    st.header("2. API setup")
    st.write("Add your Gemini API key to a `.env` file or environment variable named `GEMINI_API_KEY`.")
    st.link_button("Get a Gemini API key", "https://aistudio.google.com/apikey")

if not API_KEY:
    st.info("First, set your GEMINI_API_KEY environment variable. See README.md for steps.")
    st.stop()

if not uploaded_files:
    st.info("Upload at least one PDF or TXT document from the left sidebar to begin.")
    st.stop()

all_chunks = []
source_names = []
for uploaded in uploaded_files:
    try:
        extracted_text = read_uploaded_file(uploaded)
        chunks = split_into_chunks(extracted_text)
        all_chunks.extend(chunks)
        source_names.extend([uploaded.name] * len(chunks))
    except Exception as exc:
        st.error(f"Couldn't read {uploaded.name}: {exc}")

if not all_chunks:
    st.warning("No readable text found. If your PDF is scanned, run OCR first or upload a text-based PDF.")
    st.stop()

# TF-IDF gives us a simple, local retrieval step without a separate vector database.
vectorizer = TfidfVectorizer(stop_words="english")
try:
    chunk_vectors = vectorizer.fit_transform(all_chunks)
except ValueError:
    st.error("The documents don't contain enough readable text to search.")
    st.stop()

st.success(f"Ready! Loaded {len(uploaded_files)} document(s) and indexed {len(all_chunks)} text chunks.")

question = st.text_input("Ask a question", placeholder="e.g., What is the attendance requirement?")
ask = st.button("Get answer", type="primary")

if ask:
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        retrieved = retrieve_chunks(question, all_chunks, vectorizer, chunk_vectors)
        if not retrieved:
            st.warning("I couldn't find a relevant passage in the uploaded documents.")
        else:
            with st.spinner("Searching the documents and preparing an answer..."):
                try:
                    client = genai.Client(api_key=API_KEY)
                    answer = answer_with_gemini(question, retrieved, client)
                    st.subheader("Answer")
                    st.write(answer)
                    with st.expander("See retrieved document passages"):
                        for i, (chunk, score) in enumerate(retrieved, start=1):
                            st.markdown(f"**Passage {i}** · relevance score: `{score:.3f}`")
                            st.write(chunk)
                except Exception as exc:
                    st.error("Something went wrong while contacting Gemini.")
                    st.caption(f"Technical detail: {exc}")
