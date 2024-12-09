import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from typing import Dict, Tuple
from strategies import run_virtual_experiments


class ExperimentApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.configure_root()
        self.initialize_parameters()

        # Основной интерфейс
        self.main_frame = tk.Frame(root, bg="#F3F4F6")
        self.main_frame.pack(fill="both", expand=True)
        self.create_layout()

    def configure_root(self) -> None:
        """Настройки основного окна."""
        self.root.title("Эксперимент по стратегическим подходам")
        self.root.geometry("1200x640")
        self.root.config(bg="#F3F4F6")

    def initialize_parameters(self) -> None:
        """Инициализация параметров эксперимента."""
        self.n = 10
        self.steps = 10
        self.switch_step = 7
        self.k = 3
        self.num_experiments = 50
        self.v_range = (0.1, 1.0)
        self.a_range = (0.12, 0.22)
        self.b_range = (0.85, 1.0)

    def create_layout(self) -> None:
        """Создание макета приложения."""
        # Левая панель для ввода параметров
        self.left_frame = tk.Frame(self.main_frame, padx=8, pady=10, bg="#D1D5DB")
        self.left_frame.pack(side="left", fill="y", padx=8, pady=10)
        self.create_input_fields()
        self.create_checkboxes()
        self.create_run_button()
        self.create_range_labels()

        # Правая панель для графика
        self.right_frame = tk.Frame(self.main_frame, padx=25, pady=10, bg="#D1D5DB")
        self.right_frame.pack(side="right", fill="both", expand=True)

    def create_input_fields(self) -> None:
        """Создание полей ввода параметров."""
        self.add_label(self.left_frame, "Настройки эксперимента", 0, font=("Calibri", 20), bg="gray", fg="white")
        self.n_entry = self.add_labeled_entry("Количество партий (n):", 1, self.n)
        self.steps_entry = self.add_labeled_entry("Количество этапов (steps):", 2, self.steps)
        self.v_entry = self.add_labeled_entry("Влияние дозировки (v):", 3, self.v_range[0])
        self.a_entry = self.add_labeled_entry("Начальная сахаристость (a):", 4, self.a_range[0])
        self.b_entry = self.add_labeled_entry("Коэффициент деградации (b):", 5, self.b_range[0])

    def add_label(self, parent: tk.Widget, text: str, row: int, **kwargs) -> None:
        """Добавление текста метки."""
        label = tk.Label(parent, text=text, anchor="w", **kwargs)
        label.grid(row=row, columnspan=2, pady=10, sticky="w")

    def add_labeled_entry(self, label_text: str, row: int, default_value: float) -> tk.Entry:
        """Создание поля ввода с меткой."""
        label = tk.Label(self.left_frame, text=label_text, font=("Calibri", 14), bg="gray", fg="white", anchor="w")
        label.grid(row=row, column=0, sticky="w", padx=10)
        entry = tk.Entry(self.left_frame, validate="key", bg="white", fg="black")
        entry.grid(row=row, column=1, padx=10, sticky="w")
        entry.insert(0, str(default_value))
        return entry

    def create_checkboxes(self) -> None:
        """Добавление чекбоксов."""
        self.inorganic_checkbox_var = tk.BooleanVar()
        self.add_checkbox("Учитывать неорганические вещества", 11, self.inorganic_checkbox_var)

        self.dosage_checkbox_var = tk.BooleanVar()
        self.add_checkbox("Использовать дозаривание", 12, self.dosage_checkbox_var)

    def add_checkbox(self, text: str, row: int, variable: tk.BooleanVar) -> None:
        """Создание чекбокса."""
        checkbox = tk.Checkbutton(self.left_frame, text=text, variable=variable, 
                                  bg="#D1D5DB", fg="#111827", font=("Calibri", 13), anchor="w")
        checkbox.grid(row=row, columnspan=2, pady=10)

    def create_range_labels(self) -> None:
        """Добавление надписи с диапазонами параметров."""
        range_text = (
            f"Интервалы для задания параметров:\n"
            f"   v ({self.v_range[0]} - {self.v_range[1]}), "
            f"a ({self.a_range[0]} - {self.a_range[1]}), "
            f"b ({self.b_range[0]} - {self.b_range[1]})"
        )
        self.add_label(self.left_frame, range_text, 10, font=("Calibri", 14), bg="#D1D5DB", fg="#111827")

    def create_run_button(self) -> None:
        """Добавление кнопки запуска эксперимента."""
        self.run_button = tk.Button(
            self.left_frame, text="Запустить эксперимент", command=self.on_run_button_click,
            bg="#3B82F6", fg="white", font=("Calibri", 15)
        )
        self.run_button.grid(row=14, columnspan=2, pady=25)

    def on_run_button_click(self) -> None:
        """Обработка нажатия кнопки запуска."""
        # Получение параметров
        if not self.get_parameters():
            return

        # Запуск экспериментов
        results = run_virtual_experiments(
            self.num_experiments, self.n, self.steps, self.switch_step, self.k,
            self.a_range, self.b_range, self.inorganic_checkbox_var.get(), self.dosage_checkbox_var.get()
        )
        self.update_graph(results)

    def get_parameters(self) -> bool:
        """Получение и валидация параметров из полей ввода."""
        try:
            self.n = int(self.n_entry.get())
            self.steps = int(self.steps_entry.get())
            self.v = float(self.v_entry.get())
            self.a_init = float(self.a_entry.get())
            self.b_deg = float(self.b_entry.get())
            if not (self.v_range[0] <= self.v <= self.v_range[1]):
                raise ValueError(f"Значение v должно быть в пределах {self.v_range}.")
            if not (self.a_range[0] <= self.a_init <= self.a_range[1]):
                raise ValueError(f"Значение a должно быть в пределах {self.a_range}.")
            if not (self.b_range[0] <= self.b_deg <= self.b_range[1]):
                raise ValueError(f"Значение b должно быть в пределах {self.b_range}.")
            return True
        except ValueError as e:
            messagebox.showerror("Ошибка ввода", str(e))
            return False

    def determine_best_strategy(self, results: dict[str, dict[str, float]]) -> tuple[str, float, float]:
        """Определяет лучшую стратегию на основе результатов."""
        best_strategy = None
        max_sugar = -float("inf")
        min_losses = float("inf")

        for strategy, data in results.items():
            sugar = data['sugar']
            losses = data['losses']
            # Критерий: максимизируем выход сахара и минимизируем потери
            if sugar > max_sugar or (sugar == max_sugar and losses < min_losses):
                best_strategy = strategy
                max_sugar = sugar
                min_losses = losses

        return best_strategy, max_sugar, min_losses
    
    def update_graph(self, results: dict[str, dict[str, float]]) -> None:
        """Обновление графика на основе результатов эксперимента."""
        strategies = list(results.keys())
        sugar_values = [results[strategy]['sugar'] for strategy in strategies]
        losses_values = [results[strategy]['losses'] for strategy in strategies]

        fig, ax = plt.subplots(figsize=(20, 6))  # Увеличиваем ширину графика

        x = range(len(strategies))

        # Построение графика
        ax.bar(x, sugar_values, width=0.5, label="Выход сахара", align='center', color='green')
        ax.bar(x, losses_values, width=0.5, label="Относительные потери", align='edge', color='red')

        ax.set_xlabel("Стратегия")
        ax.set_ylabel("Значение")
        ax.set_title("Сравнение стратегий по выходу сахара и потерям")
        ax.set_xticks(x)
        ax.set_xticklabels(strategies, rotation=45)
        ax.legend()
        ax.grid(axis='y')

        fig.patch.set_facecolor('#F3F4F6')  # Фон для всего графика

        # Определяем лучшую стратегию
        best_strategy, max_sugar, min_losses = self.determine_best_strategy(results)  # Здесь используем self
        best_label = f"Лучшая стратегия: {best_strategy}\nВыход сахара: {max_sugar:.2f}, Потери: {min_losses:.2f}"
        ax.text(0.95, 0.95, best_label, transform=ax.transAxes, fontsize=10, color='blue', 
                verticalalignment='top', horizontalalignment='right', bbox=dict(facecolor='white', alpha=0.7))

        # Удаляем старое изображение и добавляем новое
        for widget in self.right_frame.winfo_children():
            widget.destroy()

        # Встраиваем график в интерфейс
        canvas = FigureCanvasTkAgg(fig, master=self.right_frame)
        canvas.draw()

        # Устанавливаем цвет фона самого canvas
        canvas.get_tk_widget().config(bg='#F3F4F6')  # Фон для самого холста

        # Размещение графика с учетом доступной ширины
        canvas.get_tk_widget().pack(fill='both', expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = ExperimentApp(root)
    root.mainloop()
