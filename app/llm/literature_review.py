import ollama


def generate_literature_review(text):

    prompt = f"""
You are an expert research assistant.

Analyze the following document and generate a structured literature review.

Use the following sections:

# Research Problem

# Background

# Methodology

# Key Findings

# Strengths

# Limitations

# Future Work

Document:

{text}

Literature Review:
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
