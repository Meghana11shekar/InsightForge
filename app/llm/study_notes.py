import ollama


def generate_study_notes(text):

    prompt = f"""
You are an AI tutor.

Create well-structured study notes from the document.

Use this format:

# Overview

# Important Concepts

# Key Definitions

# Examples (if available)

# Quick Revision Points

Document:

{text}

Study Notes:
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
