import requests
import json

CONFIG_PATH = "/ai_system/core/config.json"

def load_config():
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)

def ask_ollama(prompt):
    try:
        response = requests.post(
            "http://127.0.0.1:11434/api/generate",
            json={
                "model": "mistral",
                "prompt": prompt,
                "stream": False
            }
        )
        return response.json()["response"]
    except Exception as e:
        return f"Error: {e}"

def run_lone(task):
    config = load_config()

    prompt = f"""
You are {config['ai_name']}.
Always address the user as {config['master_name']}.

User request:
{task}
"""

    answer = ask_ollama(prompt)

    if not answer:
        return "No response generated."

    return answer.replace("Khan Saab", "KHAN SAAB")
