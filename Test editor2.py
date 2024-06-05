import tkinter as tk
from tkinter import filedialog
from ttkthemes import ThemedStyle
import subprocess
def open_file():
    filepath = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if filepath:
        with open(filepath, "r", encoding="utf-8") as file:
            text = file.read()
            text_area.delete(1.0, tk.END)
            text_area.insert(1.0, text)
def back():
    root.destroy()
    subprocess.Popen(["python", "Test.py"])
def save_file():
    filepath = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if filepath:
        with open(filepath, "w", encoding="utf-8") as file:
            text = text_area.get(1.0, tk.END)
            file.write(text)
def switch_language():
    global language
    language = "en" if language == "ru" else "ru"
    update_texts()
def update_texts():
    open_button.config(text=texts["open_button"][language])
    save_button.config(text=texts["save_button"][language])
    exit_button.config(text=texts["exit_button"][language])
    language_button.config(text=texts["language_button"][language])
root = tk.Tk()
root.title("Text Editor")
texts = {
    "open_button": {"ru": "Открыть", "en": "Open"},
    "save_button": {"ru": "Сохранить", "en": "Save"},
    "exit_button": {"ru": "Вернуться", "en": "Back"},
    "language_button": {"ru": "Switch to English", "en": "Переключить на русский"},}
language = "ru"
text_area = tk.Text(root, wrap="word")
text_area.pack(expand=True, fill="both")
open_button = tk.Button(root, text=texts["open_button"][language], command=open_file)
open_button.pack(side=tk.LEFT, padx=5, pady=5)
save_button = tk.Button(root, text=texts["save_button"][language], command=save_file)
save_button.pack(side=tk.LEFT, padx=5, pady=5)
exit_button = tk.Button(root, text=texts["exit_button"][language], command=back)
exit_button.pack(side=tk.LEFT, padx=5, pady=5)
language_button = tk.Button(root, text=texts["language_button"][language], command=switch_language)
language_button.pack(side=tk.LEFT, padx=5, pady=5)
style = ThemedStyle(root)
style.set_theme("ubuntu")
root.mainloop()