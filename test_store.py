from ingestion.chunker import chunk_text
from embeddings.embedder import embed
from vectorstore.store import add_chunks, search

text = """
Cross-validation splits the data into k folds. The model trains on k-1 folds
and tests on the remaining one. This repeats k times so every fold serves as
the test set once. The scores are averaged to give a more reliable estimate
than a single train-test split.

Gradient descent is an optimization algorithm. It computes the gradient of the
loss with respect to each parameter, then steps in the opposite direction to
reduce the loss. The learning rate controls how large each step is.

Overfitting happens when a model memorizes the training data instead of
learning general patterns. It shows up as a large gap between training accuracy
and validation accuracy. Regularization and more data both help reduce it.
"""

chunks = chunk_text(text, chunk_size=40, overlap=10)
print(f"Created {len(chunks)} chunks")

vectors = embed(chunks)
count = add_chunks(chunks, vectors)
print(f"Stored. Collection now has {count} items")
print()

question = "how do I know if my model memorized the training data?"
question_vector = embed([question])[0]

docs, distances = search(question_vector, n_results=2)

print(f"Question: {question}")
print()
for doc, dist in zip(docs, distances):
    print(f"[distance {dist:.3f}]  {doc[:120]}...")
    print()