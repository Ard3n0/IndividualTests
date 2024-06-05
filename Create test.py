import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from ttkthemes import ThemedStyle
import subprocess
def create_question_file():
    global language
    language = "ru"
    texts = {
        "time_label": {"ru": "Длительность теста (в минутах):", "en": "Test duration (in minutes):"},
        "prompt_label": {"ru": "Вопрос:", "en": "Question:"},
        "options_label": {"ru": "Варианты ответов (2-10):", "en": "Answer options (2-10):"},
        "correct_option_label": {"ru": "Номер правильного ответа:", "en": "Correct answer number:"},
        "add_button": {"ru": "Добавить вопрос", "en": "Add question"},
        "save_button": {"ru": "Сохранить файл", "en": "Save file"},
        "back_button": {"ru": "Вернуться", "en": "Back"},
        "question_list_label": {"ru": "Добавленные вопросы:", "en": "Added questions:"},
        "info_label": {"ru": "", "en": ""},
        "error_label": {"ru": "", "en": ""},
        "option_error": {"ru": "Нельзя добавить больше 10 вариантов ответа",
                         "en": "Cannot add more than 10 answer options"},
        "question_error": {"ru": "Нужно как минимум 2 варианта ответа", "en": "Need at least 2 answer options"},
        "file_success": {"ru": "Файл '{file_path}' успешно создан.", "en": "File '{file_path}' created successfully."},
        "question_info_title": {"ru": "Информация о вопросе", "en": "Question info"},
        "question_text": {"ru": "Вопрос: {prompt}\n\n", "en": "Question: {prompt}\n\n"},
        "option_text": {"ru": "Вариант {i}: {option}", "en": "Option {i}: {option}"},
        "correct_option_text": {"ru": "\n\nНомер правильного ответа: {correct_option}",
                                "en": "\n\nCorrect answer number: {correct_option}"},}
    def switch_language():
        global language
        language = "en" if language == "ru" else "ru"
        for widget in root.winfo_children():
            widget.destroy()
        create_widgets()
    def add_question():
        if len(option_entries) < 2:
            error_label.config(text=texts["question_error"][language])
            return
        elif len(option_entries) > 10:
            error_label.config(text=texts["option_error"][language])
            return
        else:
            error_label.config(text="")
        question_num = len(questions) + 1
        prompt = prompt_entry.get()
        options = [option_entry.get() for option_entry in option_entries]
        correct_option = int(correct_option_entry.get())
        questions.append((question_num, prompt, options, correct_option))
        update_question_list()
    def update_question_list():
        question_list.delete(0, tk.END)
        for question in questions:
            question_list.insert(tk.END, question[1])
    def clear_entries():
        prompt_entry.delete(0, tk.END)
        for option_label in option_labels:
            option_label.grid_forget()
            option_label.destroy()
        for option_entry in option_entries:
            option_entry.grid_forget()
            option_entry.destroy()
        option_labels.clear()
        option_entries.clear()
        correct_option_entry.delete(0, tk.END)
    def save_file():
        file_path = filedialog.asksaveasfilename(defaultextension=".txt")
        if file_path:
            time_limit = time_entry.get()
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(str(time_limit) + "\n")
                for question_num, prompt, options, correct_option in questions:
                    file.write(str(question_num) + "\n")
                    file.write(prompt + "\n")
                    for option in options:
                        file.write(option + "\n")
                    file.write("###\n")
                    file.write(str(correct_option) + "\n")
            info_label.config(text=texts["file_success"][language].format(file_path=file_path))
    def back():
        root.destroy()
        subprocess.Popen(["python", "Test.py"])
    def add_option_entry():
        if len(option_entries) < 10:
            new_row = len(option_entries) + 2
            new_option_label = ttk.Label(root, text=f"{texts['options_label'][language]} {len(option_entries) + 1}:")
            new_option_label.grid(row=new_row, column=0, padx=5, pady=5, sticky="w")
            new_option_entry = ttk.Entry(root, width=20)
            new_option_entry.grid(row=new_row, column=1, padx=5, pady=5)
            option_labels.append(new_option_label)
            option_entries.append(new_option_entry)
        else:
            error_label.config(text=texts["option_error"][language])
    def remove_option_entry():
        if len(option_entries) > 2:
            last_option_label = option_labels.pop()
            last_option_label.grid_forget()
            last_option_label.destroy()
            last_entry = option_entries.pop()
            last_entry.grid_forget()
            last_entry.destroy()
        else:
            error_label.config(text=texts["question_error"][language])
    def show_question_info(event):
        selection = question_list.curselection()
        if selection:
            index = selection[0]
            question_info = questions[index]
            question_text = texts["question_text"][language].format(prompt=question_info[1])
            options_text = "\n".join([texts["option_text"][language].format(i=i + 1, option=option) for i, option in
                                      enumerate(question_info[2])])
            correct_option_text = texts["correct_option_text"][language].format(correct_option=question_info[3])
            messagebox.showinfo(texts["question_info_title"][language],
                                question_text + options_text + correct_option_text)
    def create_widgets():
        global time_entry, prompt_entry, option_entries, option_labels, correct_option_entry, question_list, info_label, error_label
        time_label = ttk.Label(root, text=texts["time_label"][language])
        time_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        time_entry = ttk.Entry(root, width=10)
        time_entry.grid(row=0, column=1, padx=5, pady=5)
        prompt_label = ttk.Label(root, text=texts["prompt_label"][language])
        prompt_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        prompt_entry = ttk.Entry(root, width=40)
        prompt_entry.grid(row=1, column=1, padx=5, pady=5)
        options_label = ttk.Label(root, text=texts["options_label"][language])
        options_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        add_option_button = ttk.Button(root, text="+", command=add_option_entry)
        add_option_button.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        remove_option_button = ttk.Button(root, text="-", command=remove_option_entry)
        remove_option_button.grid(row=2, column=2, padx=5, pady=5, sticky="w")
        option_entries = []
        option_labels = []
        for i in range(2):
            option_label = ttk.Label(root, text=f"{texts['options_label'][language]} {i + 1}:")
            option_label.grid(row=3 + i, column=0, padx=5, pady=5, sticky="w")
            option_labels.append(option_label)
            option_entry = ttk.Entry(root, width=20)
            option_entry.grid(row=3 + i, column=1, padx=5, pady=5)
            option_entries.append(option_entry)
        correct_option_label = ttk.Label(root, text=texts["correct_option_label"][language])
        correct_option_label.grid(row=3, column=2, padx=5, pady=5, sticky="w")
        correct_option_entry = ttk.Entry(root, width=10)
        correct_option_entry.grid(row=3, column=3, padx=5, pady=5)
        add_button = ttk.Button(root, text=texts["add_button"][language], command=add_question)
        add_button.grid(row=4, column=3, padx=5, pady=5)
        save_button = ttk.Button(root, text=texts["save_button"][language], command=save_file)
        save_button.grid(row=5, column=3, padx=5, pady=5)
        back_button = ttk.Button(root, text=texts["back_button"][language], command=back)
        back_button.grid(row=8, column=3, padx=5, pady=5)
        info_label = ttk.Label(root, text=texts["info_label"][language])
        info_label.grid(row=6, column=3, padx=5, pady=5)
        error_label = ttk.Label(root, text=texts["error_label"][language], foreground="red")
        error_label.grid(row=7, column=3, padx=5, pady=5)
        question_list_label = ttk.Label(root, text=texts["question_list_label"][language])
        question_list_label.grid(row=0, column=4, padx=5, pady=5, sticky="w")
        question_list = tk.Listbox(root, width=40, height=10)
        question_list.grid(row=1, column=4, rowspan=7, padx=5, pady=5, sticky="nsew")
        question_list.bind("<Double-Button-1>", show_question_info)
        scrollbar = ttk.Scrollbar(root, orient="vertical", command=question_list.yview)
        scrollbar.grid(row=1, column=5, rowspan=7, padx=(0, 5), pady=5, sticky="ns")
        question_list.config(yscrollcommand=scrollbar.set)
        language_button = ttk.Button(root, text="Switch to English" if language == "ru" else "Переключить на русский",
                                     command=switch_language)
        language_button.grid(row=9, column=3, padx=5, pady=5)
    root = tk.Tk()
    root.title("Создание файла с вопросами")
    root.geometry("1000x425")
    questions = []
    option_entries = []
    option_labels = []
    create_widgets()
    style = ThemedStyle(root)
    style.set_theme("plastik")
    root.mainloop()
create_question_file()