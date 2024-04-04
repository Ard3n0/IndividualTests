import tkinter as tk
from tkinter import ttk, filedialog
from ttkthemes import ThemedStyle
import subprocess

class Question:
    def __init__(self, prompt, options, correct_option, time_limit=None):
        self.prompt = prompt
        self.options = options
        self.correct_option = correct_option
        self.user_answer = tk.StringVar()
        self.time_limit = time_limit

def load_questions(file_path):
    questions = []
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        if lines:
            total_time = int(lines[0].strip()) * 60
            i = 1
            while i < len(lines):
                line = lines[i].strip('\n')
                try:
                    question_number = int(line)
                    i += 1
                    if i < len(lines):
                        prompt = lines[i].strip()
                        i += 1
                        options = []
                        while i < len(lines) and lines[i].strip() != "###":
                            if lines[i].strip():
                                options.append(lines[i].strip())
                            i += 1
                        correct_option = None
                        if i < len(lines) and lines[i].strip() == "###":
                            i += 1
                            if i < len(lines):
                                correct_option_str = lines[i].strip()
                                if correct_option_str:
                                    correct_option = int(correct_option_str) - 1
                                i += 1
                        question = Question(prompt, options, correct_option, time_limit=None)
                        questions.append(question)
                except ValueError:
                    i += 1
            return questions, total_time
        else:
            return [], 0

def create_main_window():
    def create_test():
        subprocess.Popen(["python", "Create test.py"])

    def test_editor():
        subprocess.Popen(["python", "Test editor2.py"])

    def analyze_test():
        subprocess.Popen(["python", "Tests_analyze.py"])

    def select_file(root):
        file_path = filedialog.askopenfilename(
            title="Выберите файл с вопросами",
            filetypes=[("Text Files", "*.txt")]
        )
        if file_path:
            questions, total_time = load_questions(file_path)
            start_quiz(questions, root, total_time)
            create_test_button.pack_forget()
            test_editor_button.pack_forget()

    def start_quiz(questions, root, total_time):
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

        start_timer(root, finish_button, total_time)

    def start_timer(root, finish_button, total_time):
        global timer_running, timer_id
        timer_running = False
        timer_label = ttk.Label(root, text=f"Оставшееся время: {total_time // 60} мин {total_time % 60} сек")
        timer_label.pack()
        countdown(root, finish_button, total_time, timer_label)

    def countdown(root, finish_button, total_time, timer_label):
        global timer_id, timer_running
        if total_time > 0:
            minutes, seconds = divmod(total_time, 60)
            try:
                timer_label.config(text=f"Оставшееся время: {minutes} мин {seconds} сек")
            except tk.TclError:
                stop_timer()
                return
            timer_id = root.after(1000, countdown, root, finish_button, total_time - 1, timer_label)
            timer_running = True
        else:
            stop_timer()
            finish_button.invoke()

    def stop_timer():
        global timer_running
        if timer_running:
            root.after_cancel(timer_id)
            timer_running = False

    def show_results(questions, root):
        stop_timer()
        for widget in root.winfo_children():
            widget.destroy()

        result_list = tk.Listbox(root, width=60, height=10)
        result_list.pack()

        score, user_answers = run_quiz(questions, result_list)

        result_label = ttk.Label(root, text=f"Количество правильных ответов: {score} из {len(questions)}")
        result_label.pack()

        save_button = ttk.Button(root, text="Сохранить результаты", command=lambda: save_results(score, user_answers, questions))
        save_button.pack()

        show_answers_button = ttk.Button(root, text="Показать ответы", command=lambda: show_answers(user_answers, root))
        show_answers_button.pack()

        close_button = ttk.Button(root, text="Закрыть", command=lambda: [stop_timer(), root.destroy()])
        close_button.pack()

    def run_quiz(questions, result_list):
        score = 0
        user_answers = []
        for i, question in enumerate(questions, 1):
            ans = question.user_answer.get()
            if ans:
                user_answer = f"Ваш ответ: {question.options[int(ans)]}"
                is_correct = ans == str(question.correct_option)
            else:
                user_answer = "Вы не выбрали ответ"
                is_correct = False
            score += is_correct
            if question.correct_option is not None:
                correct_option_index = question.correct_option
                if correct_option_index < len(question.options):
                    correct_option = question.options[correct_option_index]
                else:
                    correct_option = "Недоступно"
            else:
                correct_option = "Правильный ответ отсутствует"
            user_answers.append((user_answer, is_correct, correct_option))
            result_list.insert(tk.END, f"{user_answer}\n")
            result_list.insert(tk.END, f"   Правильно" if is_correct else "   Неправильно.")
            result_list.insert(tk.END, "\n")
        return score, user_answers

    def save_results(score, user_answers, questions):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if file_path:
            correct_answers = [(question.options[question.correct_option],) if question.correct_option is not None else ("Правильный ответ отсутствует",) for question in questions]
            save_results_to_file(score, user_answers, correct_answers, file_path)

    def save_results_to_file(score, user_answers, correct_answers, file_path):
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(f"Количество правильных ответов: {score} из {len(correct_answers)}\n\n")
            file.write("Ваши ответы:\n")
            for i, (user_answer, is_correct, _) in enumerate(user_answers, 1):
                file.write(f"{i}. {user_answer}\n")
                file.write(f"   {'Правильно' if is_correct else 'Неправильно'}\n")
            file.write("\nПравильные ответы:\n")
            for i, (correct_answer,) in enumerate(correct_answers, 1):
                file.write(f"{i}. {correct_answer}\n")

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
            elif user_answer == "Вы не выбрали ответ":
                answers_list.insert(tk.END, "Вы не выбрали ответ")
            else:
                if correct_option == "Правильный ответ отсутствует":
                    answers_list.insert(tk.END, correct_option)
                else:
                    answers_list.insert(tk.END, f"Правильный ответ: {correct_option}")
            answers_list.insert(tk.END, "")

        close_button = ttk.Button(answers_window, text="Закрыть", command=answers_window.destroy)
        close_button.pack()

    root = tk.Tk()
    root.title("OffTes")

    root.geometry("500x400")

    style = ThemedStyle(root)
    style.set_theme("ubuntu")

    select_file_button = ttk.Button(root, text="Выбрать файл", command=lambda: select_file(root))
    select_file_button.pack()

    create_test_button = ttk.Button(root, text="Создать тест", command=create_test)
    create_test_button.pack()

    test_editor_button = ttk.Button(root, text="Отредактировать тест", command=test_editor)
    test_editor_button.pack()

    test_editor_button = ttk.Button(root, text="Просмотреть результаты", command=analyze_test)
    test_editor_button.pack()

    root.mainloop()

if __name__ == "__main__":
    create_main_window()
