import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from visualization import plot_results  # Импортируем функцию визуализации
from strategies import run_virtual_experiments

class ExperimentApp: 
    def __init__(self, root):
        self.root = root
        self.root.title("Эксперимент по стратегическим подходам")
        self.root.geometry("1200x640")
        
        # Фон окна
        self.root.config(bg='#F3F4F6')

        self.n = 10
        self.steps = 10
        self.switch_step = 7
        self.k = 3
        self.num_experiments = 50

        self.v_range = (0.1, 1.0)
        self.a_range = (0.12, 0.22)
        self.b_range = (0.85, 1.0)
        
        # Основной фрейм для настройки и графика
        self.main_frame = tk.Frame(root, bg='#F3F4F6')
        self.main_frame.pack(fill='both', expand=True)

        # Разделение на две колонки: левая (ввод параметров) и правая (график)
        self.left_frame = tk.Frame(self.main_frame, padx=8, pady=10, bg='#D1D5DB') 
        self.left_frame.pack(side='left', fill='y', padx=8, pady=10)
        
        self.right_frame = tk.Frame(self.main_frame, padx=25, pady=10, bg='#D1D5DB')
        self.right_frame.pack(side='right', fill='both', expand=True)
        
        # Создаем поля ввода в левой части
        self.create_input_fields()
        self.create_checkboxes()
        self.create_run_button()
        self.create_range_labels()

    def create_input_fields(self):
        """Функция для создания полей ввода."""
        label = tk.Label(self.left_frame, text="Настройки эксперимента", font=("calibri", 20), bg='gray', fg='white', anchor='w')
        label.grid(row=0, columnspan=2, pady=10, sticky='w')
        
        # Поля ввода с проверкой
        self.n_label = tk.Label(self.left_frame, text="Количество партий (n):", font=("calibri", 14), bg='gray', fg='white', anchor='w')
        self.n_label.grid(row=1, column=0, sticky="w", padx=10)
        self.n_entry = tk.Entry(self.left_frame, validate='key', bg='white', fg='black')
        self.n_entry.grid(row=1, column=1, padx=10, sticky="w")
        self.n_entry.insert(0, str(self.n))
        
        self.steps_label = tk.Label(self.left_frame, text="Количество этапов (steps):", font=("calibri", 14), bg='gray', fg='white', anchor='w')
        self.steps_label.grid(row=2, column=0, sticky="w", padx=10)
        self.steps_entry = tk.Entry(self.left_frame, validate='key', bg='white', fg='black')
        self.steps_entry.grid(row=2, column=1, padx=10, sticky="w")
        self.steps_entry.insert(0, str(self.steps))
        
        self.v_label = tk.Label(self.left_frame, text="Влияние дозировки (v):", font=("calibri", 14), bg='gray', fg='white', anchor='w')
        self.v_label.grid(row=3, column=0, sticky="w", padx=10)
        self.v_entry = tk.Entry(self.left_frame, validate='key', bg='white', fg='black')
        self.v_entry.grid(row=3, column=1, padx=10, sticky="w")
        self.v_entry.insert(0, str(self.v_range[0]))

        self.a_label = tk.Label(self.left_frame, text="Начальная сахаристость (a):", font=("calibri", 14), bg='gray', fg='white', anchor='w')
        self.a_label.grid(row=4, column=0, sticky="w", padx=10)
        self.a_entry = tk.Entry(self.left_frame, validate='key', bg='white', fg='black')
        self.a_entry.grid(row=4, column=1, padx=10, sticky="w")
        self.a_entry.insert(0, str(self.a_range[0]))
        
        self.b_label = tk.Label(self.left_frame, text="Коэффициент деградации (b):", font=("calibri", 14), bg='gray', fg='white', anchor='w')
        self.b_label.grid(row=5, column=0, sticky="w", padx=10)
        self.b_entry = tk.Entry(self.left_frame, validate='key', bg='white', fg='black')
        self.b_entry.grid(row=5, column=1, padx=10, sticky="w")
        self.b_entry.insert(0, str(self.b_range[0]))

    def create_range_labels(self):
        """Функция для создания надписей с диапазонами параметров."""
        range_label = tk.Label(self.left_frame, 
                               text=f"Интервалы для задания параметров: \n   v ({self.v_range[0]} - {self.v_range[1]}),"
                                    f"a ({self.a_range[0]} - {self.a_range[1]}), "
                                    f"b ({self.b_range[0]} - {self.b_range[1]})", 
                               font=("calibri", 14), bg='#D1D5DB', fg='#111827', anchor='w')
        range_label.grid(row=10, columnspan=2, pady=10, sticky='w')

    def create_checkboxes(self):
        """Добавление чекбоксов для учета дозаривания и неорганических веществ."""
        # Чекбокс для учета неорганических веществ
        self.inorganic_checkbox_var = tk.BooleanVar()
        self.inorganic_checkbox = tk.Checkbutton(self.left_frame, 
                                                 text="Учитывать неорганические вещества", 
                                                 variable=self.inorganic_checkbox_var, 
                                                 bg='#D1D5DB', fg='#111827', anchor='w',  font=("calibri", 13))
        self.inorganic_checkbox.grid(row=11, columnspan=2, pady=10)

        # Чекбокс для учета дозаривания
        self.dosage_checkbox_var = tk.BooleanVar()
        self.dosage_checkbox = tk.Checkbutton(self.left_frame, 
                                              text="Использовать дозаривание", 
                                              variable=self.dosage_checkbox_var, 
                                              bg='#D1D5DB', fg='#111827', anchor='w',  font=("calibri", 13))
        self.dosage_checkbox.grid(row=12, columnspan=2, pady=10)

    def create_run_button(self):
        """Добавление кнопки для запуска эксперимента."""
        self.run_button = tk.Button(self.left_frame, text="Запустить эксперимент", command=self.on_run_button_click, 
                                    bg='#3B82F6', fg='white', anchor='w', font=("calibri", 15))  # Цвет кнопки изменен
        self.run_button.grid(row=14, columnspan=2, pady=25)

    def on_run_button_click(self):
        # Получаем значения из чекбоксов
        inorganic_influence = self.inorganic_checkbox_var.get()
        dosage = self.dosage_checkbox_var.get()
        print("Эксперимент запущен!")

        # Если дозаривание не выбрано, получаем значения параметров
        if not dosage:
            try:
                self.n = int(self.n_entry.get())
                self.v = float(self.v_entry.get())
                self.a_init = float(self.a_entry.get())
                self.b_deg = float(self.b_entry.get())
                
                # Проверяем, что введенные значения находятся в заданных диапазонах
                if not (self.v_range[0] <= self.v <= self.v_range[1]):
                    messagebox.showerror("Ошибка", f"Значение для v должно быть в пределах {self.v_range[0]} - {self.v_range[1]}.")
                    return
                if not (self.a_range[0] <= self.a_init <= self.a_range[1]):
                    messagebox.showerror("Ошибка", f"Значение для a должно быть в пределах {self.a_range[0]} - {self.a_range[1]}.")
                    return
                if not (self.b_range[0] <= self.b_deg <= self.b_range[1]):
                    messagebox.showerror("Ошибка", f"Значение для b должно быть в пределах {self.b_range[0]} - {self.b_range[1]}.")
                    return

            except ValueError:
                messagebox.showerror("Ошибка ввода", "Пожалуйста, введите правильные значения для всех параметров.")
                return

        # Передаем правильное количество аргументов
        results = run_virtual_experiments(self.num_experiments, self.n, self.steps, self.switch_step, self.k,
                                        self.a_range, self.b_range, inorganic_influence, dosage)

        self.update_graph(results)

    def update_graph(self, results):
        """Обновление графика на основе результатов эксперимента с использованием функции plot_results."""
        plot_results(results)


# Основной запуск
if __name__ == "__main__":
    root = tk.Tk()
    app = ExperimentApp(root)
    root.mainloop()