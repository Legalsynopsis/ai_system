import tkinter as tk
from tkinter import scrolledtext
import os

# Import LONE brain
from brain import run_lone as brain_run

# ==============================
# MAIN WINDOW
# ==============================

root = tk.Tk()
root.title("LONE AI - KHAN SAAB")
root.geometry("900x600")

# ==============================
# FUNCTIONS
# ==============================

def run_lone():
    task = entry.get()

    if not task.strip():
        output.insert(tk.END, "⚠️ Enter a task\n\n")
        return

    output.insert(tk.END, f"\n🧠 You: {task}\n")

    try:
        answer = brain_run(task)
        output.insert(tk.END, f"🤖 LONE: {answer}\n\n")
    except Exception as e:
        output.insert(tk.END, f"❌ Error: {e}\n")


def open_recordroom():
    os.system("xdg-open /ai_system/data/RecordRoom")


def start_downloader():
    output.insert(tk.END, "\n📥 Starting Record Downloader...\n")
    os.system("python /ai_system/core/lone_record_system.py")

# ==============================
# UI DESIGN
# ==============================

# Title
title = tk.Label(root, text="LONE AI SYSTEM", font=("Arial", 18, "bold"))
title.pack(pady=10)

# Input box
entry = tk.Entry(root, width=80, font=("Arial", 12))
entry.pack(pady=10)

# Buttons frame
frame = tk.Frame(root)
frame.pack()

btn_run = tk.Button(frame, text="Run LONE", command=run_lone, width=15)
btn_run.grid(row=0, column=0, padx=10)

btn_open = tk.Button(frame, text="Open RecordRoom", command=open_recordroom, width=18)
btn_open.grid(row=0, column=1, padx=10)

btn_download = tk.Button(frame, text="Start Downloader", command=start_downloader, width=18)
btn_download.grid(row=0, column=2, padx=10)

# Output box
output = scrolledtext.ScrolledText(root, width=100, height=25, font=("Arial", 10))
output.pack(pady=10)

# ==============================
# RUN APP
# ==============================

root.mainloop()
