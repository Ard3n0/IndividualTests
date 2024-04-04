import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from ttkthemes import ThemedStyle

def create_question_file():
    questions = []

    def add_question():
        if len(option_entries) < 2:
            error_label.config(text="Нужно как минимум 2 варианта ответа")
            return
        elif len(option_entries) > 10:
            error_label.config(text="Нельзя добавить больше 10 вариантов ответа")
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
            info_label.config(text=f"Файл '{file_path}' успешно создан.")

    def add_option_entry():
        if len(option_entries) < 10:
            new_row = len(option_entries) + 2
            new_option_label = ttk.Label(root, text=f"Вариант {len(option_entries) + 1}:")
            new_option_label.grid(row=new_row, column=0, padx=5, pady=5, sticky="w")
            new_option_entry = ttk.Entry(root, width=20)
            new_option_entry.grid(row=new_row, column=1, padx=5, pady=5)
            option_labels.append(new_option_label)
            option_entries.append(new_option_entry)
        else:
            error_label.config(text="Нельзя добавить больше 10 вариантов ответа")

    def remove_option_entry():
        if len(option_entries) > 2:
            last_option_label = option_labels.pop()
            last_option_label.grid_forget()
            last_option_label.destroy()
            last_entry = option_entries.pop()
            last_entry.grid_forget()
            last_entry.destroy()
        else:
            error_label.config(text="Нужно как минимум 2 варианта ответа")

    def show_question_info(event):
        selection = question_list.curselection()
        if selection:
            index = selection[0]
            question_info = questions[index]
            question_text = f"Вопрос: {question_info[1]}\n\n"
            options_text = "\n".join([f"Вариант {i + 1}: {option}" for i, option in enumerate(question_info[2])])
            correct_option_text = f"\n\nНомер правильного ответа: {question_info[3]}"
            messagebox.showinfo("Информация о вопросе", question_text + options_text + correct_option_text)

    root = tk.Tk()
    root.title("Создание файла с вопросами")
    root.geometry("1000x425")

    time_label = ttk.Label(root, text="Длительность теста (в минутах):")
    time_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
    time_entry = ttk.Entry(root, width=10)
    time_entry.grid(row=0, column=1, padx=5, pady=5)

    prompt_label = ttk.Label(root, text="Вопрос:")
    prompt_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
    prompt_entry = ttk.Entry(root, width=40)
    prompt_entry.grid(row=1, column=1, padx=5, pady=5)

    options_label = ttk.Label(root, text="Варианты ответов(2-10):")
    options_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
    add_option_button = ttk.Button(root, text="+", command=lambda: add_option_entry())
    add_option_button.grid(row=2, column=1, padx=5, pady=5, sticky="w")
    remove_option_button = ttk.Button(root, text="-", command=lambda: remove_option_entry())
    remove_option_button.grid(row=2, column=2, padx=5, pady=5, sticky="w")

    option_entries = []
    option_labels = []
    for i in range(2):
        option_label = ttk.Label(root, text=f"Вариант {i + 1}:")
        option_label.grid(row=3+i, column=0, padx=5, pady=5, sticky="w")
        option_labels.append(option_label)
        option_entry = ttk.Entry(root, width=20)
        option_entry.grid(row=3+i, column=1, padx=5, pady=5)
        option_entries.append(option_entry)

    correct_option_label = ttk.Label(root, text="Номер правильного ответа:")
    correct_option_label.grid(row=3, column=2, padx=5, pady=5, sticky="w")
    correct_option_entry = ttk.Entry(root, width=10)
    correct_option_entry.grid(row=3, column=3, padx=5, pady=5)

    add_button = ttk.Button(root, text="Добавить вопрос", command=add_question)
    add_button.grid(row=4, column=3, padx=5, pady=5)

    save_button = ttk.Button(root, text="Сохранить файл", command=save_file)
    save_button.grid(row=5, column=3, padx=5, pady=5)

    info_label = ttk.Label(root, text="")
    info_label.grid(row=6, column=3, padx=5, pady=5)

    error_label = ttk.Label(root, text="", foreground="red")
    error_label.grid(row=7, column=3, padx=5, pady=5)

    question_list_label = ttk.Label(root, text="Добавленные вопросы:")
    question_list_label.grid(row=0, column=4, padx=5, pady=5, sticky="w")
    question_list = tk.Listbox(root, width=40, height=10)
    question_list.grid(row=1, column=4, rowspan=7, padx=5, pady=5, sticky="nsew")
    question_list.bind("<Double-Button-1>", show_question_info)
    scrollbar = ttk.Scrollbar(root, orient="vertical", command=question_list.yview)
    scrollbar.grid(row=1, column=5, rowspan=7, padx=(0, 5), pady=5, sticky="ns")
    question_list.config(yscrollcommand=scrollbar.set)

    style = ThemedStyle(root)
    style.set_theme("plastik")

    root.mainloop()

create_question_file()