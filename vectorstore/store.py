import chromadb

DB_PATH = "chroma_db"
COLLECTION_NAME = "notes"


def get_collection():
    client = chromadb.PersistentClient(path=DB_PATH)
    return client.get_or_create_collection(name=COLLECTION_NAME)


def add_chunks(chunks, vectors):
    collection = get_collection()
    ids = [f"chunk_{i}" for i in range(len(chunks))]

    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=vectors.tolist(),
    )
    return collection.count()


def search(question_vector, n_results=3):
    collection = get_collection()

    results = collection.query(
        query_embeddings=[question_vector.tolist()],
        n_results=n_results,
    )

    return results["documents"][0], results["distances"][0]