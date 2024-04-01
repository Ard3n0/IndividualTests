import tkinter as tk
from tkinter import ttk, filedialog

class Question:
    def __init__(self, prompt, options, correct_option):
        self.prompt = prompt
        self.options = options
        self.correct_option = correct_option
        self.user_answer = tk.StringVar()

def load_questions(file_path):
    questions = []
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        for i in range(0, len(lines), 6):
            prompt = lines[i].strip()
            options = [line.strip() for line in lines[i+1:i+4]]
            correct_option = int(lines[i+4].split(':')[1])
            question = Question(prompt, options, correct_option-1)
            questions.append(question)
    return questions

def select_file():
    file_path = filedialog.askopenfilename(
        title="Выберите файл с вопросами",
        filetypes=[("Text Files", "*.txt")]
    )
    if file_path:
        questions = load_questions(file_path)
        start_quiz(questions, root)

def run_quiz(questions, result_list):
    score = 0
    user_answers = []
    for i, question in enumerate(questions, 1):
        ans = question.user_answer.get()
        user_answer = f"Ваш ответ: {question.options[int(ans)]}"
        is_correct = ans == str(question.correct_option)
        score += is_correct
        correct_option_index = question.correct_option
        if correct_option_index < len(question.options):
            correct_option = question.options[correct_option_index]
        else:
            correct_option = "Недоступно"
        user_answers.append((user_answer, is_correct, correct_option))
        result_list.insert(tk.END, f"{user_answer}\n")
        result_list.insert(tk.END, f"   Правильно" if is_correct else "   Неправильно.")
        result_list.insert(tk.END, "\n")
    return score, user_answers

def show_results(questions, root):
    result_window = tk.Toplevel(root)
    result_window.title("Результат")
    result_window.geometry("800x600")

    style = ttk.Style(result_window)
    style.configure("TLabel", font=("Arial", 12), padding=10)
    style.configure("TButton", font=("Arial", 12), padding=5)

    result_list = tk.Listbox(result_window, width=60, height=10)
    result_list.pack()  # Добавленная строка

    score, user_answers = run_quiz(questions, result_list)

    result_label = ttk.Label(result_window, text=f"Количество правильных ответов: {score} из {len(questions)}")
    result_label.pack()

    show_answers_button = ttk.Button(result_window, text="Показать ответы", command=lambda: show_answers(user_answers, result_window))
    show_answers_button.pack()

    close_button = ttk.Button(result_window, text="Закрыть", command=result_window.destroy)
    close_button.pack()

    result_list.pack()  # Добавленная строка


def show_answers(user_answers, root):
    answers_window = tk.Toplevel(root)
    answers_window.title("Правильные ответы")
    answers_window.geometry("400x300")

    answers_list = tk.Listbox(answers_window, width=40, height=10)
    answers_list.pack()

    for i, (user_answer, is_correct, correct_option) in enumerate(user_answers, 1):
        answers_list.insert(tk.END, f"{i}. {user_answer}")
        if is_correct:
            answers_list.insert(tk.END, f"Ответ верный!")
        else:
            answers_list.insert(tk.END, f"Правильный ответ: {correct_option}")
        answers_list.insert(tk.END, "")

    close_button = ttk.Button(answers_window, text="Закрыть", command=answers_window.destroy)
    close_button.pack()

def start_quiz(questions, root):
    for question in questions:
        prompt_label = ttk.Label(root, text=question.prompt, style="TLabel")
        prompt_label.pack(anchor=tk.W)

        for i, option in enumerate(question.options):
            option_button = ttk.Radiobutton(root, text=option, variable=question.user_answer, value=str(i))
            option_button.pack(anchor=tk.W)

        separator = tk.Frame(root, height=2, bd=1, relief=tk.SUNKEN)
        separator.pack(fill=tk.X, padx=5, pady=5)

    finish_button = ttk.Button(root, text="Завершить", command=lambda: show_results(questions, root), style="TButton")
    finish_button.pack()

root = tk.Tk()
root.title("Тест")

select_file_button = ttk.Button(root, text="Выбрать файл", command=select_file)
select_file_button.pack()

root.mainloop()