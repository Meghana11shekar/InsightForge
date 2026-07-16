import ollama


def extract_keywords(text):

    prompt = f"""
You are an AI research assistant.

Extract the 10-15 most important keywords from this document.

Rules:
- Return ONLY the keywords.
- One keyword per line.
- Do not number them.

Document:

{text}

Keywords:
"""

    response = ollama.chat(
        model="qwen2.5:7b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]
