import json
import random

from vectorstore.store import get_collection
from generation.answer import client, MODEL

N_QUESTIONS = 30
OUTPUT = "eval/questions.json"

PROMPT = """Here is a passage from a research paper:

{chunk}

Write one specific question that this passage answers. Requirements:
- It must be answerable from this passage alone.
- Do not reuse distinctive phrases from the passage — write it the way a
  reader would ask, using different wording.
- Do not refer to "the passage" or "the text".

Reply with the question only, nothing else."""

collection = get_collection()
data = collection.get()
chunks = data["documents"]
ids = data["ids"]

print(f"Corpus has {len(chunks)} chunks")

indices = random.sample(range(len(chunks)), min(N_QUESTIONS, len(chunks)))
questions = []

for n, i in enumerate(indices, 1):
    response = client.messages.create(
        model=MODEL,
        max_tokens=200,
        messages=[{"role": "user", "content": PROMPT.format(chunk=chunks[i])}],
    )
    question = response.content[0].text.strip()

    questions.append({"question": question, "expected_id": ids[i]})
    print(f"{n}/{len(indices)}: {question}")

with open(OUTPUT, "w", encoding="utf-8") as f:
    json.dump(questions, f, indent=2, ensure_ascii=False)

print(f"\nSaved {len(questions)} questions to {OUTPUT}")