import os

from groq import Groq


class LLMService:

    def __init__(self):

        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise ValueError(
                "GROQ_API_KEY environment variable is not set."
            )

        self.client = Groq(
            api_key=api_key
        )

    def generate(
        self,
        question: str,
        context: str
    ) -> str:

        prompt = f"""
You are a financial analysis assistant.

Answer the user's question using only the provided context.

If the context does not contain enough information,
say that the information is not available.

Context:
{context}

Question:
{question}
"""

        response = self.client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0
        )

        return response.choices[0].message.content