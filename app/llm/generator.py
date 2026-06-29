import ollama


def generate_answer(question, context):

    prompt = f"""
You are an AI research assistant.

Answer ONLY using the context below.

If the answer is not present, say:
"I couldn't find that information in the uploaded document."

Context:
{context}

Question:
{question}

Answer:
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
