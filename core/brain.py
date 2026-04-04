import requests
import json
import os

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


# 🧠 MAIN AI
def run_lone(task):
    config = load_config()

    prompt = f"""
You are {config['ai_name']}, a Karnataka Revenue Department expert.

STRICT RULES:
- Always interpret terms in LAND / PROPERTY context
- "Mutation" means RTC / land record transfer (NOT politics)
- Ignore political meanings completely
- Answer like a government officer
- Give step-by-step practical process

Knowledge Areas:
- Karnataka Land Revenue Act
- Bhoomi / RTC / Mutation
- Survey (Mojini)
- Kaveri Registration
- Panchayat Raj / e-Swathu
- BDA / BBMP / Municipal laws

Always address user as {config['master_name']}.

User Question:
{task}
"""

    answer = ask_ollama(prompt)

    if not answer:
        return "No response generated."

    return answer.replace("Khan Saab", "KHAN SAAB")


# 📂 SMART DOCUMENT HANDLER
def handle_document(file_path):
    try:
        if not os.path.exists(file_path):
            return "File not found."

        text = ""

        # 🔹 TRY METHOD 1: PyPDF2
        try:
            from PyPDF2 import PdfReader
            reader = PdfReader(file_path)

            for page in reader.pages:
                text += page.extract_text() or ""

        except:
            text = ""

        # 🔹 IF EMPTY → TRY METHOD 2 (RAW READ)
        if not text.strip():
            try:
                with open(file_path, "rb") as f:
                    raw = f.read(5000)
                    text = str(raw)
            except:
                pass

        # 🔹 STILL EMPTY
        if not text.strip():
            return """
⚠️ KHAN SAAB:

This PDF is likely:
- Scanned document
- Image-based
- Not readable by text extractor

👉 Next upgrade will enable OCR (image reading)
"""

        text = text[:3000]

        prompt = f"""
You are a Karnataka legal expert.

Analyze this document and explain clearly:

{text}
"""

        answer = ask_ollama(prompt)

        return f"\n📄 DOCUMENT ANALYSIS:\n{answer}"

    except Exception as e:
        return f"Error reading document: {e}"


def main():
    config = load_config()

    print(f"\nAt your service, {config['master_name']}")

    while True:
        try:
            task = input("\nEnter task: ")
            if task.lower() in ["exit", "quit"]:
                print("Goodbye KHAN SAAB 👑")
                break

            result = run_lone(task)
            print(f"\nLONE: {result}")

        except KeyboardInterrupt:
            print("\nStopped by user.")
            break


if __name__ == "__main__":
    main()
