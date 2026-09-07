from embeddings.embedder import embed
from vectorstore.store import search
from generation.answer import answer

print("StudyBot ready. Type 'quit' to exit.\n")

while True:
    question = input("You: ").strip()

    if question.lower() in ("quit", "exit"):
        break

    if not question:
        continue

    question_vector = embed([question])[0]
    chunks, distances = search(question_vector, n_results=3)

    reply = answer(chunks, question)

    print(f"\nStudyBot: {reply}\n")