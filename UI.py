import tkinter as tk
from tkinter import ttk

# Создание корневого окна
root = tk.Tk()
root.title("Тест")

# Создание стиля
style = ttk.Style()

# Импорт темы оформления
style.theme_use("clam")  # Возможные варианты: "default", "alt", "clam", "classic"

# Настройка цветов и других параметров
style.configure("TButton", foreground="white", background="blue")
style.configure("TLabel", foreground="black", background="light gray")
style.configure("TRadiobutton", foreground="blue")

# Добавление виджетов
label = ttk.Label(root, text="Это пример применения темы оформления", padding=10)
label.pack()

button = ttk.Button(root, text="Кнопка", padding=10)
button.pack()

radio1 = ttk.Radiobutton(root, text="Вариант 1", value=1)
radio1.pack()

radio2 = ttk.Radiobutton(root, text="Вариант 2", value=2)
radio2.pack()

# Запуск главного цикла событий
root.mainloop()