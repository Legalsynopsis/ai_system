import requests
import json
from doc_reader import read_document, translate_text
from record_brain import search_documents

CONFIG_PATH = "/ai_system/core/config.json"


def load_config():
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)


def ask_ollama(prompt):
    response = requests.post(
        "http://127.0.0.1:11434/api/generate",
        json={"model": "mistral", "prompt": prompt, "stream": False}
    )
    return response.json()["response"]


def run_lone(task):
    config = load_config()

    docs = search_documents(task)

    context = ""

    for doc in docs:
        content = read_document(doc)
        context += content[:1000]

    translated = translate_text(context)

    prompt = f"""
You are {config['ai_name']}, Karnataka Legal AI.

Answer using below context only:

{translated}

Question:
{task}
"""

    answer = ask_ollama(prompt)

    return answer.replace("Khan Saab", "KHAN SAAB")
