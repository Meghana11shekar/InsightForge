import ollama


def summarize_document(text):

    prompt = f"""
You are an AI research assistant.

Write a clear summary of the document.

Include:

• Main topic

• Key points

• Important conclusions

Document:

{text}

Summary:
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
