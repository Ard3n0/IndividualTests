import tkinter as tk
from tkinter import filedialog
from ttkthemes import ThemedStyle

def open_file():
    filepath = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if filepath:
        with open(filepath, "r", encoding="utf-8") as file:
            text = file.read()
            text_area.delete(1.0, tk.END)
            text_area.insert(1.0, text)

def save_file():
    filepath = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if filepath:
        with open(filepath, "w", encoding="utf-8") as file:
            text = text_area.get(1.0, tk.END)
            file.write(text)

root = tk.Tk()
root.title("Text Editor")

text_area = tk.Text(root, wrap="word")
text_area.pack(expand=True, fill="both")

open_button = tk.Button(root, text="Открыть", command=open_file)
open_button.pack(side=tk.LEFT, padx=5, pady=5)

save_button = tk.Button(root, text="Сохранить", command=save_file)
save_button.pack(side=tk.LEFT, padx=5, pady=5)

exit_button = tk.Button(root, text="Выйти", command=root.destroy)
exit_button.pack(side=tk.LEFT, padx=5, pady=5)

style = ThemedStyle(root)
style.set_theme("ubuntu")

root.mainloop()