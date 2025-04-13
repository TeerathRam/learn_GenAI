from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = OpenAI(api_key=os.getenv("GEMINI_API_KEY"),
base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

system_prompt = """
You are an AI assistance who is expert in breaking down comlex problems and then resolve.

For the given user input, analyse the input and break down the problem step by step.

Atleast think 5-6 steps on how to solve the problem before solving it down.

The steps are you get a user input, you analyse, you think, you think again for several times and then return an output with explanation and then finally you validate the output as well before giving final result.

Follow the steps in sequence that is "analyse", "think", "output", "validate" and finally result.

Rules:
1. Follow the strict JSON as per Output schema.
2. Always perform one step at a time and wait for next input.
3. Carefully analyse the user query.

Output Format: {{ step: "string", content: "string"}}

Example:
Input: What is 2 + 2.
Output: {{step: "analyse", content: "Alright! The user is intrested in maths query and he is asking basic arthematic operation"}}
Output: {{step: "think", content: "To perform the addition i must go from left to right and add all the operands"}}
Output: {{step: "output", content: "4"}}
Output: {{step: "validate", content: "seems like 4 is correct ans for 2 + 2"}}
Output: {{step: "result", content: "2 + 2 = 4 and that is calculated by adding all numbers"}}
"""

result = client.chat.completions.create(
model="gemini-2.0-flash",
response_format={"type": "json_object"},
messages=[
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": "What is 2 + 3 * 6?  Explain briefly"},

    #
    {"role": "assistant", "content": json.dumps({
    "step": "analyse",
    "content": "The user is asking to evaluate a mathematical expression that involves addition and multiplication. It's important to consider the order of operations (PEMDAS/BODMAS)."
    })},
    {"role": "assistant", "content": json.dumps({
    "step": "think",
    "content": "The order of operations dictates that multiplication should be performed before addition. Therefore, I should first calculate 3 * 6 and then add 2 to the result."
    })},
    {"role": "assistant", "content": json.dumps({
    "step": "output",
    "content": "First, calculate 3 * 6 = 18. Then, add 2 to the result: 2 + 18 = 20."
    })}
]
)

print(result.choices[0].message.content)