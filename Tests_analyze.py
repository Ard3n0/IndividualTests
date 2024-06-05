import os
import tkinter as tk
from tkinter import ttk, filedialog
from ttkthemes import ThemedStyle
import sys
class TestResultsAnalyzer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Результаты теста")
        self.results_directory = "results"
        self.result_files = []
        self.user_stats = {}
        self.language = "ru"
        self.texts = {
            "load_button": {"ru": "Загрузить файл с результатами", "en": "Load Results File"},
            "results_label": {"ru": "Загруженные файлы:", "en": "Loaded Files:"},
            "full_info_label": {"ru": "Информация о результатах:", "en": "Results Information:"},
            "open_file_button": {"ru": "Вернуться", "en": "Back"},
            "language_button": {"ru": "Switch to English", "en": "Переключить на русский"},
            "file_dialog_title": {"ru": "Выберите файл с результатами теста", "en": "Select Test Results File"},
            "file_dialog_type": {"ru": "Text Files", "en": "Text Files"},
            "treeview_heading": {"ru": "Имя файла", "en": "Filename"},}
        self.create_widgets()
        self.style = ThemedStyle(self)
        self.style.set_theme("plastik")
    def analyze_results(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            try:
                return lines
            except Exception as e:
                print("Error parsing result file:", e)
                return None
    def load_results_file(self):
        file_path = filedialog.askopenfilename(
            title=self.texts["file_dialog_title"][self.language],
            filetypes=[(self.texts["file_dialog_type"][self.language], "*.txt")])
        if file_path:
            lines = self.analyze_results(file_path)
            if lines is not None:
                filename = os.path.basename(file_path)
                self.user_stats[filename] = lines
                self.update_results_tree()
    def update_results_tree(self):
        self.results_tree.delete(*self.results_tree.get_children())
        for filename in self.user_stats.keys():
            self.results_tree.insert("", "end", text=filename, iid=filename)
    def show_full_info(self, event):
        filename = self.results_tree.selection()[0]
        lines = self.user_stats[filename]
        self.full_info_text.config(state=tk.NORMAL)
        self.full_info_text.delete(1.0, tk.END)
        for line in lines:
            self.full_info_text.insert(tk.END, line)
        self.full_info_text.config(state=tk.DISABLED)
    def open_file(self):
        other_file = "Test.py"
        os.execl(sys.executable, sys.executable, other_file)
    def switch_language(self):
        self.language = "en" if self.language == "ru" else "ru"
        self.update_texts()
    def update_texts(self):
        self.load_button.config(text=self.texts["load_button"][self.language])
        self.results_label.config(text=self.texts["results_label"][self.language])
        self.full_info_label.config(text=self.texts["full_info_label"][self.language])
        self.open_file_button.config(text=self.texts["open_file_button"][self.language])
        self.results_tree.heading("#0", text=self.texts["treeview_heading"][self.language])
        self.language_button.config(text=self.texts["language_button"][self.language])
    def create_widgets(self):
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(side=tk.LEFT, padx=20, pady=20)
        self.main_frame.columnconfigure(0, weight=1)
        self.load_button = ttk.Button(self.main_frame, text=self.texts["load_button"][self.language], command=self.load_results_file)
        self.load_button.grid(row=0, column=0, padx=5, pady=5)
        self.results_label = ttk.Label(self.main_frame, text=self.texts["results_label"][self.language])
        self.results_label.grid(row=1, column=0, padx=5, pady=5)
        self.results_tree = ttk.Treeview(self.main_frame)
        self.results_tree.heading("#0", text=self.texts["treeview_heading"][self.language])
        self.results_tree.column("#0", width=400)
        self.results_tree.grid(row=2, column=0, padx=5, pady=5)
        self.results_tree.bind("<Double-1>", self.show_full_info)
        self.info_frame = ttk.Frame(self)
        self.info_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=20, pady=20)
        self.full_info_label = ttk.Label(self.info_frame, text=self.texts["full_info_label"][self.language])
        self.full_info_label.pack(pady=(0, 5))
        self.full_info_text = tk.Text(self.info_frame, wrap=tk.WORD)
        self.full_info_text.pack(fill=tk.BOTH, expand=True)
        self.open_file_button = ttk.Button(self.main_frame, text=self.texts["open_file_button"][self.language], command=self.open_file)
        self.open_file_button.grid(row=3, column=0, padx=5, pady=5)
        self.language_button = ttk.Button(self.main_frame, text=self.texts["language_button"][self.language], command=self.switch_language)
        self.language_button.grid(row=4, column=0, padx=5, pady=5)
if __name__ == "__main__":
    app = TestResultsAnalyzer()
    app.mainloop()