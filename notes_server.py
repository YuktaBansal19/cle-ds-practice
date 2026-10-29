from pathlib import Path
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Notes Server")
NOTES_FOLDER = Path(__file__).parent / "notes"


@mcp.tool()
def list_notes() -> list[str]:
    """List all text notes."""
    NOTES_FOLDER.mkdir(exist_ok=True)
    return sorted(file.name for file in NOTES_FOLDER.glob("*.txt"))


@mcp.tool()
def read_note(filename: str) -> str:
    """Read one note by its filename, for example todo.txt."""
    safe_name = Path(filename).name
    if safe_name != filename or not safe_name.endswith(".txt"):
        return "Please provide a simple .txt filename, such as todo.txt."

    path = NOTES_FOLDER / safe_name
    if not path.exists():
        return f"Note not found: {safe_name}"
    return path.read_text(encoding="utf-8")


@mcp.tool()
def search_notes(keyword: str) -> list[str]:
    """Find notes whose text contains a keyword."""
    NOTES_FOLDER.mkdir(exist_ok=True)
    matches = []
    for path in sorted(NOTES_FOLDER.glob("*.txt")):
        if keyword.lower() in path.read_text(encoding="utf-8").lower():
            matches.append(path.name)
    return matches


if __name__ == "__main__":
    mcp.run()
