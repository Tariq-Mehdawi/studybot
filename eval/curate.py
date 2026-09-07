import json

INPUT = "eval/questions.json"
OUTPUT = "eval/questions_curated.json"

EXCLUDE_PHRASES = [
    "what year was",
    "what conference published",
    "how long does it take",
    "what percentage",
    "cost per document",
    "how many attacks",
    "how many different large language models",
    "achieved the highest",
    "supplementary experimental results",
]

with open(INPUT, encoding="utf-8") as f:
    questions = json.load(f)

kept = []
removed = []

for item in questions:
    q = item["question"].lower()
    if any(phrase in q for phrase in EXCLUDE_PHRASES):
        removed.append(item["question"])
    else:
        kept.append(item)

with open(OUTPUT, "w", encoding="utf-8") as f:
    json.dump(kept, f, indent=2, ensure_ascii=False)

print(f"Kept {len(kept)}, removed {len(removed)}\n")
print("Removed (bibliography / table lookup, not comprehension):")
for q in removed:
    print(f"  - {q}")
print(f"\nSaved to {OUTPUT}")