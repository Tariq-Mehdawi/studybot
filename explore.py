from embeddings.embedder import embed

sentences = [
    "White blood cells attack invading pathogens.",
    "The immune system fights off bacteria and viruses.",
    "Barcelona won the match three goals to one.",
    "The football team scored three times in the final.",
        "The model predicts the outcome accurately.",
    "The model does not predict the outcome accurately.",
]

vectors = embed(sentences)

print("Shape:", vectors.shape)
print()

similarity = vectors @ vectors.T

for i, row in enumerate(similarity):
    scores = "  ".join(f"{v:.2f}" for v in row)
    print(f"s{i}:  {scores}")