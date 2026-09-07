from ingestion.chunker import chunk_text

text = " ".join(f"word{i}" for i in range(1, 1001))

chunks = chunk_text(text, chunk_size=300, overlap=50)

print(f"Total words: 1000")
print(f"Number of chunks: {len(chunks)}")
print()

for i, c in enumerate(chunks):
    words = c.split()
    print(f"chunk {i}: starts '{words[0]}'  ends '{words[-1]}'  ({len(words)} words)")