import ollama


def generate_research_gap(text):

    prompt = f"""
You are an experienced research analyst.

Analyze the following document and identify possible research gaps.

Generate your response using this format:

# Existing Work

# Identified Research Gaps

# Limitations

# Suggested Improvements

# Future Research Opportunities

Document:

{text}

Research Gap Analysis:
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
