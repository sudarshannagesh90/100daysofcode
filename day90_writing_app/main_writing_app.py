import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import time

window = tk.Tk()
window.title('Writing-app')
window.geometry('400x400+200+200')

text_editor = ScrolledText()
text_editor.pack()
last_text = text_editor.get("1.0", tk.END)


def pass_function(x):
    global last_text
    next_text = text_editor.get("1.0", tk.END)
    if last_text == next_text:
        text_editor.delete("1.0", tk.END)
        last_text = ''
    else:
        last_text = next_text
    window.after(5000, pass_function, x - 1)


pass_function(10000000000)
window.mainloop()
