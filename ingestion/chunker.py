def chunk_text(text, chunk_size=300, overlap=50):
    words = text.split()
    step = chunk_size - overlap

    chunks = []
    start = 0

    while start < len(words):
        piece = words[start:start + chunk_size]
        chunks.append(" ".join(piece))
        start += step

    return chunks