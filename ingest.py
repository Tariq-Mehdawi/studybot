import shutil
import os

from ingestion.loader import load_folder
from ingestion.chunker import chunk_text
from embeddings.embedder import embed
from vectorstore.store import add_chunks

DATA_FOLDER = "data"
DB_PATH = "chroma_db"

if os.path.exists(DB_PATH):
    shutil.rmtree(DB_PATH)
    print("Cleared old database")

documents = load_folder(DATA_FOLDER)
print(f"Loaded {len(documents)} files")

all_chunks = []

for filename, text in documents.items():
    chunks = chunk_text(text, chunk_size=300, overlap=50)
    all_chunks.extend(chunks)
    print(f"  {filename}: {len(text.split())} words → {len(chunks)} chunks")

print(f"\nTotal chunks: {len(all_chunks)}")
print("Embedding...")

vectors = embed(all_chunks)
count = add_chunks(all_chunks, vectors)

print(f"Done. Stored {count} chunks.")