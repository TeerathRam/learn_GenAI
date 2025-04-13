from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()

text = "Eiffel Tower is in Paris and is a famous landmark, it is 345 meters tall"

client = OpenAI(api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/")

response = client.embeddings.create(input=text, model="text-embedding-3-small", dimensions=3)

print(response.data[0].embedding)