import tkinter as tk
from tkinter import scrolledtext, filedialog
from brain import run_lone as brain_run, handle_document
import threading

# ==============================
# WINDOW
# ==============================

root = tk.Tk()
root.title("LONE AI - KHAN SAAB")
root.geometry("950x700")
root.configure(bg="#121212")

# ==============================
# CHAT BOX
# ==============================

chat_box = scrolledtext.ScrolledText(
    root,
    bg="#1e1e1e",
    fg="white",
    font=("Segoe UI", 11),
    wrap=tk.WORD,
    bd=0,
    padx=10,
    pady=10
)
chat_box.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# ==============================
# INPUT FRAME
# ==============================

input_frame = tk.Frame(root, bg="#121212")
input_frame.pack(fill=tk.X, padx=10, pady=10)

entry = tk.Entry(
    input_frame,
    font=("Segoe UI", 12),
    bg="#2b2b2b",
    fg="white",
    insertbackground="white",
    bd=0
)
entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=10, padx=(0,10))

# ==============================
# FUNCTIONS
# ==============================

def process_task(task):
    chat_box.insert(tk.END, f"\n🧠 KHAN SAAB:\n{task}\n\n", "user")

    try:
        response = brain_run(task)
        chat_box.insert(tk.END, f"🤖 LONE:\n{response}\n\n", "bot")
    except Exception as e:
        chat_box.insert(tk.END, f"❌ Error: {e}\n\n")

    chat_box.yview(tk.END)


def run_lone():
    task = entry.get()
    entry.delete(0, tk.END)

    if not task.strip():
        return

    threading.Thread(target=process_task, args=(task,)).start()


def upload_file():
    file_path = filedialog.askopenfilename()

    if not file_path:
        return

    chat_box.insert(tk.END, f"\n📄 FILE SELECTED:\n{file_path}\n\n", "user")

    def process_file():
        try:
            result = handle_document(file_path)
            chat_box.insert(tk.END, f"🤖 LONE (Document Analysis):\n{result}\n\n", "bot")
        except Exception as e:
            chat_box.insert(tk.END, f"❌ Error: {e}\n\n")

        chat_box.yview(tk.END)

    threading.Thread(target=process_file).start()

# ==============================
# BUTTONS
# ==============================

send_btn = tk.Button(
    input_frame,
    text="Send",
    command=run_lone,
    bg="#00C853",
    fg="black",
    font=("Segoe UI", 10, "bold"),
    bd=0,
    padx=20,
    pady=10
)
send_btn.pack(side=tk.RIGHT)

upload_btn = tk.Button(
    input_frame,
    text="Upload",
    command=upload_file,
    bg="#2196F3",
    fg="white",
    font=("Segoe UI", 10, "bold"),
    bd=0,
    padx=20,
    pady=10
)
upload_btn.pack(side=tk.RIGHT, padx=5)

# ==============================
# STYLES
# ==============================

chat_box.tag_config("user", foreground="#00E5FF")
chat_box.tag_config("bot", foreground="#FFD54F")

# ENTER KEY SUPPORT
root.bind('<Return>', lambda event: run_lone())

# START MESSAGE
chat_box.insert(tk.END, "🤖 LONE READY, KHAN SAAB...\n\n", "bot")

# ==============================
# RUN
# ==============================

root.mainloop()
