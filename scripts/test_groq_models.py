import os

from groq import Groq


client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


models = client.models.list()


print("Available models:\n")

for model in models.data:

    print(model.id)