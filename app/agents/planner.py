import ollama


class PlannerAgent:

    def plan(self, task):

        prompt = f"""
You are an AI planner.

Break this task into simple execution steps.

Task:

{task}

Return ONLY a numbered list.
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
