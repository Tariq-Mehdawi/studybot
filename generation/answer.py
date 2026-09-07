import os
from dotenv import load_dotenv
import anthropic

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

MODEL = "claude-sonnet-4-5"


PROMPT_TEMPLATE = """Here is context from the user's study notes:

{context}

Using only the context above, answer this question:
{question}

Be concise. Match the length of your answer to the complexity of the question — a simple question gets one or two sentences, not a structured breakdown. Only use headings or bullet points when the answer genuinely has multiple distinct parts.

If the context does not contain the answer, reply with exactly this and nothing else:
"Not covered in the documents."
"""


def build_prompt(chunks, question):
    context = "\n\n---\n\n".join(chunks)
    return PROMPT_TEMPLATE.format(context=context, question=question)


def answer(chunks, question):
    prompt = build_prompt(chunks, question)

    response = client.messages.create(
        model=MODEL,
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}],
    )

    return response.content[0].text