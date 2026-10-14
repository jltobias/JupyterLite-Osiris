"""Execute and save all exercise notebooks so the Book includes their figures."""
from pathlib import Path
import nbformat
from nbclient import NotebookClient

for path in sorted((Path(__file__).resolve().parents[1] / "content").glob("*.ipynb")):
    notebook = nbformat.read(path, as_version=4)
    NotebookClient(notebook, timeout=120, kernel_name="python3").execute()
    nbformat.write(notebook, path)
    print(f"Executed {path.name}")
