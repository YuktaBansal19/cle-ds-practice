# College FAQ Bot — Beginner RAG Project

A small Retrieval-Augmented Generation (RAG) app. Upload a college syllabus, handbook, or FAQ document, then ask questions about it.

## How RAG works here

1. **Load:** read text from uploaded PDF/TXT documents.
2. **Chunk:** split the text into smaller overlapping passages.
3. **Retrieve:** TF-IDF searches for the passages most relevant to the question.
4. **Generate:** Gemini uses those passages to write an answer.
5. **Grounding:** the prompt tells Gemini not to invent answers if the documents do not contain the information.

This is a beginner-friendly RAG implementation. TF-IDF is used for retrieval instead of a vector database, so there is less setup.

## 1. Install Python

Use Python 3.10 or newer. Open a terminal in this folder.

## 2. Create and activate a virtual environment (recommended)

### Windows
```powershell
py -m venv .venv
.venv\Scripts\activate
```

### macOS/Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

## 4. Get a Gemini API key

Create a key at https://aistudio.google.com/apikey

Copy `.env.example` to a file named `.env` in this project folder, then replace the example value with your key. The app loads this file automatically. Alternatively, set the environment variable in your terminal.

### Windows PowerShell
```powershell
$env:GEMINI_API_KEY="paste_your_key_here"
```

### macOS/Linux
```bash
export GEMINI_API_KEY="paste_your_key_here"
```

Do not share your API key or upload it to GitHub.

## 5. Run the app

```bash
streamlit run app.py
```

A browser tab should open. Upload one or more PDF/TXT documents in the sidebar and ask a question.

## Try questions like

- What is the attendance requirement?
- Which subjects are included in the syllabus?
- What is the procedure for applying for leave?

The answer depends entirely on the document you upload. These example questions will only work if the document contains the relevant information.

## Important notes

- Use real public documents, or documents you have permission to use.
- Text-based PDFs work best. Scanned PDFs may need OCR before upload.
- The app sends the question and retrieved passages to the Gemini API to generate an answer.
- If no relevant passage is found, the app asks you to try another question.
- API usage may be subject to Google's current quotas and pricing.

## Project structure

```text
college_faq_rag_bot/
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
└── documents/
```

## What you can explain in an interview

**RAG** combines information retrieval with a language model. Instead of asking the model to answer from memory alone, the app first retrieves relevant text from the supplied documents and then gives that text to the model as context. This can make answers more specific to the documents and reduce unsupported answers.
