import os
from pypdf import PdfReader


def load_txt(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def load_pdf(path):
    reader = PdfReader(path)
    pages = [page.extract_text() or "" for page in reader.pages]
    return "\n\n".join(pages)


def load_folder(folder):
    documents = {}

    for filename in os.listdir(folder):
        path = os.path.join(folder, filename)

        if filename.endswith(".txt"):
            documents[filename] = load_txt(path)
        elif filename.endswith(".pdf"):
            documents[filename] = load_pdf(path)

    return documents