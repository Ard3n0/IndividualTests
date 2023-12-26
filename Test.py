import tkinter as tk
from tkinter import ttk

class Question:
    def __init__(self, prompt, options, correct_option):
        self.prompt = prompt
        self.options = options
        self.correct_option = correct_option
        self.user_answer = tk.StringVar()

def run_quiz(Vopros, ResList):
    ResList.delete(0, tk.END)
    sc = 0
    for i, Vopros in enumerate(Vopros, 1):
        ans = Vopros.user_answer.get()
        UserAnswer = f"{i}. Ваш ответ: {Vopros.options[int(ans)]}"
        CorrectAnswer = ans == str(Vopros.correct_option)
        sc += CorrectAnswer
        ResList.insert(tk.END, f"{UserAnswer}\n")
        ResList.insert(tk.END, f"   Правильно" if CorrectAnswer else f"   Неправильно.")
        ResList.insert(tk.END, f" " if CorrectAnswer else f" Правильный ответ: {Vopros.options[Vopros.correct_option]}\n")
        ResList.insert(tk.END, "\n")
    return sc

def show_results(questions):
    result_window = tk.Toplevel()
    result_window.title("Результат")
    result_window.geometry("800x600")

    style = ttk.Style(result_window)
    style.configure("TLabel", font=("Arial", 12), padding=10)
    style.configure("TButton", font=("Arial", 12), padding=5)

    result_list = tk.Listbox(result_window, width=60, height=10)
    result_list.pack()

    score = run_quiz(questions, result_list)

    result_label = ttk.Label(result_window, text=f"Количество правильных ответов: {score} из {len(questions)}")
    result_label.pack()

    close_button = ttk.Button(result_window, text="Закрыть", command=result_window.destroy)
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

    finish_button = ttk.Button(root, text="Завершить", command=lambda: show_results(questions), style="TButton")
    finish_button.pack()

root = tk.Tk()
root.title("Тест")

question1 = Question("Сколько будет 2+2", ["3", "4", "5"], 1)
question2 = Question("сколько будет 10 метров в см?", ["100", "500", "1000"], 2)

quiz_questions = [question1, question2]

start_quiz(quiz_questions, root)

root.mainloop()
