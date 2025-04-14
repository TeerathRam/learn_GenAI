from openai import OpenAI
from dotenv import load_dotenv
import requests
import os
import json

load_dotenv()

client = OpenAI(api_key=os.getenv("GEMINI_API_KEY"),
base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# tools to provide extra data needed
def get_weather(city: str):
    print(f"function called for {city}")

    url = f"https://wttr.in{city}?format=%C+5t"
    response = requests.get(url)
    if response.status_code == 2000:
        return f"The weather in {city} is {response.text}"
    return "Something went wrong.."

def add(x, y):
    print(f"function called for {x, y}")
    return x + y

def run_command(command: str):
    result = os.system(command=command)
    return result

available_tools = {
    "get_weather": {
        "fn": get_weather,
        "description": "Takes a city name as an input returns the current weather for the city"
    },
    "add": {
        "fn": add,
        "description": "return some of two numbers"
    },
    "run_command": {
        "fn": run_command,
        "description": "Takes a command as input to execute on system and returns ouput"
    }
}

# system prompt to set initial context to llm
system_prompt = f"""
    You are an helpful AI assistant who is  specialised in resolving user query.
    You work on start, plan, action, observe mode.
    For the given user query and available tools, plan the step by step execution, based on the planninig, select the revelent tool from the available tool. And based on the tool selection you perform an action to call the tool.
    Wait for the observation and based on the observation from the tool resolve the user query.

    Rules:
    1. Follow the strict JSON as per Output schema.
    2. Always perform one step at a time and wait for next input.
    3. Carefully analyse the user query.

    Output JSON Format:
    {{
        "step": "string",
        "content": "The name of function if the step is action",
        "input": "The input parameter for the function"
    }}

    Available Tools:
    - get_weather: Takes a city name as an input and returns the current weather for the city.
    - add: Takes two number x and y and return sum of x and y.
    - run_command: Takes a command as input to exexute on system and returns ouput.

    Example:
    User Query: What is the weather of New York?
    Output: {{ "step": "plan", "content": "The user is intrested in weather data of New York" }}
    Output: {{ "step": "plan", "content": "From the available tools I should call get_weather" }}
    Output: {{ "step": "action", "function": "get_weather", "input": "New York" }}
    Output: {{ "step": "observe", "output": "34 Degree Cel" }}
    Output: {{ "step": "output", "content": "The weather for New York seems to be 12 degrees. " }}

"""
user_query = input("> ")

message = [
    { "role": "system", "content": system_prompt}
]

message.append({ "role": "user", "content": user_query})

while True:
    response = client.chat.completions.create(
        model="gemini-2.0-flash",
        response_format={"type": "json_object"},
        messages=message
    )

    parsed_response = json.loads(response.choices[0].message.content)

    message.append({"role": "assistant", "content": json.dumps(parsed_response)})

    if parsed_response.get("step") == "plan":
        print(f"🧠: {parsed_response.get("content")}")
        continue

    if (parsed_response.get("step") == "action") and (os.system(parsed_response.get("input")) == 0):
        tool_name = parsed_response.get("function")
        tool_input = parsed_response.get("input")

        if available_tools.get(tool_name, False) != False:
            output = available_tools[tool_name].get("fn")(tool_input)
            message.append({ "role": "assistant", "content": json.dumps({ "step": "output", "content": output })})
            continue
    
    if parsed_response.get("step") == "action":
        tool_name = parsed_response.get("function")
        tool_input = parsed_response.get("input")

        if available_tools.get(tool_name, False) != False:
            output = available_tools[tool_name].get("fn")(tool_input)
            message.append({ "role": "assistant", "content": json.dumps({ "step": "output", "content": output })})
            continue


    if parsed_response.get("step") == "output":
        print(f"🤖: {parsed_response.get("content")}")
        break
    
# create a hello.txt file in current directory