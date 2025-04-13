from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

response = client.chat.completions.create(
    model="gemini-2.0-flash",
    n=1,
    messages=[
        {"role": "system", "content": "You are a helpful assistant. And you explain everything by mimicing hitesh choudhary"},
        {
            "role": "user",
            "content": "Is learning webdev is worth it?"
        }
    ]
)

print(response.choices[0].message.content)