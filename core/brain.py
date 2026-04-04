import requests
import json
from web_agent import automate_site
from scraper import extract_text

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

def main():
    config = load_config()

    print(f"\nAt your service, {config['master_name']}")

    while True:
        try:
            task = input("\nEnter task: ")

            if task.lower() in ["exit", "quit"]:
                print("Shutting down LONE...")
                break

            # 🌐 OPEN WEBSITE
            if "open website" in task.lower():
                url = task.replace("open website", "").strip()
                if not url.startswith("http"):
                    url = "https://" + url
                automate_site(url)
                continue

            # 📖 READ WEBSITE
            if "read website" in task.lower():
                url = task.replace("read website", "").strip()
                if not url.startswith("http"):
                    url = "https://" + url
                content = extract_text(url)
                print("\nLONE (DATA):", content)
                continue

            # 🤖 NORMAL AI RESPONSE
            prompt = f"""
You are {config['ai_name']}.
Always address the user as {config['master_name']}.

User request:
{task}
"""

            answer = ask_ollama(prompt)

            if not answer:
                answer = "No response generated."

            answer = answer.replace("Khan Saab", "KHAN SAAB")

            print(f"\nLONE: {answer}")

        except KeyboardInterrupt:
            print("\nShutting down LONE...")
            break

if __name__ == "__main__":
    main()
