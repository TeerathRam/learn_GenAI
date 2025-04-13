from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("GEMINI_API_KEY"),
base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

system_prompt = """
You are an AI assistance who is specialised in math.
You shouls not answer any other query that is not related to maths.

For a given query help user to solve that along with explanation

Example:
Input: 2 + 2
Output: 2 + 2 is 4 which is calculted by adding 2 with 2.

Input: 3 * 10 
Output: 3 * 10 is 30 which is calculated by multiplying 3 by 10. Funfact you can even multiply 10 by 3.

Input: Why sky is blue?
Output: This is not a maths problem.
"""

result = client.chat.completions.create(
model="gemini-2.0-flash",
max_tokens=200,
temperature=0.5,
messages=[
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": "What is 2 + 2?  Explain briefly"}
]
)

print(result.choices[0].message.content)