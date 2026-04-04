import tkinter as tk
from tkinter import filedialog
from brain import run_lone
from doc_reader import read_document, translate_text


def ask():
    q = entry.get()
    res = run_lone(q)
    output.delete("1.0", tk.END)
    output.insert(tk.END, res)


def upload():
    file = filedialog.askopenfilename()
    text = read_document(file)
    text = translate_text(text)

    output.delete("1.0", tk.END)
    output.insert(tk.END, text[:3000])


root = tk.Tk()
root.title("LONE AI")

entry = tk.Entry(root, width=80)
entry.pack()

btn = tk.Button(root, text="Ask", command=ask)
btn.pack()

upload_btn = tk.Button(root, text="Upload Document", command=upload)
upload_btn.pack()

output = tk.Text(root, height=30, width=100)
output.pack()

root.mainloop()
