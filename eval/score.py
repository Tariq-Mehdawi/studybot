import json

from retrieval.hybrid import hybrid_search
from vectorstore.store import get_collection

QUESTIONS = "eval/questions_curated.json"
K = 3

with open(QUESTIONS, encoding="utf-8") as f:
    questions = json.load(f)

collection = get_collection()
data = collection.get()
by_id = dict(zip(data["ids"], data["documents"]))

hits = 0
reciprocal_ranks = []
misses = []

for item in questions:
    returned_ids, _ = hybrid_search(item["question"], n_results=K)

    if item["expected_id"] in returned_ids:
        hits += 1
        rank = returned_ids.index(item["expected_id"]) + 1
        reciprocal_ranks.append(1 / rank)
    else:
        reciprocal_ranks.append(0)
        misses.append(item["question"])

total = len(questions)

print(f"Questions:  {total}")
print(f"Recall@{K}:   {hits / total:.2%}")
print(f"MRR:        {sum(reciprocal_ranks) / total:.2%}")

if misses:
    print(f"\nFailed to retrieve ({len(misses)}):")
    for q in misses:
        print(f"  - {q}")