import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from visualization import plot_results
from strategies import run_virtual_experiments

class GradientFrame(tk.Frame):
    def __init__(self, parent, color1, color2, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.color1 = color1
        self.color2 = color2
        self.canvas = tk.Canvas(self, width=parent.winfo_width(), height=parent.winfo_height(), highlightthickness=0)
        self.canvas.pack(fill='both', expand=True)
        self.bind("<Configure>", self._draw_gradient)

    def _draw_gradient(self, event=None):
        width = self.winfo_width()
        height = self.winfo_height()
        r1, g1, b1 = self.winfo_rgb(self.color1)
        r2, g2, b2 = self.winfo_rgb(self.color2)

        for i in range(height):
            r = int(r1 + (r2 - r1) * i / height)
            g = int(g1 + (g2 - g1) * i / height)
            b = int(b1 + (b2 - b1) * i / height)
            color = f"#{r >> 8:02x}{g >> 8:02x}{b >> 8:02x}"
            self.canvas.create_line(0, i, width, i, fill=color)

class ExperimentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Эксперимент по стратегическим подходам")
        self.root.geometry("470x600")

        self.n = 10
        self.steps = 10
        self.switch_step = 7
        self.k = 3
        self.num_experiments = 50

        self.v_range = (0.1, 1.0)
        self.a_range = (0.12, 0.22)
        self.b_range = (0.85, 1.0)

        self.main_frame = GradientFrame(root, "#1365C0", "#7EADE3")
        self.main_frame.pack(fill='both', expand=True)

        self.create_input_fields()
        self.create_checkboxes()
        self.create_run_button()
        self.create_range_labels()

    def create_input_fields(self):
        label = tk.Label(self.main_frame.canvas, text="Настройки эксперимента", font=("calibri", 20), bg='#12044E', fg='white',
                         relief="ridge", highlightbackground="#1B0773", highlightthickness=1, width=23, anchor="center")
        label.grid(row=0, columnspan=2, pady=15, padx=5)

        self.n_label = tk.Label(self.main_frame.canvas, text="Количество партий (n):", font=("calibri", 14), anchor='w', bg='#567ec2')
        self.n_label.grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.n_entry = tk.Entry(self.main_frame.canvas, validate='key', bg='white', fg='black', font=("calibri", 12))
        self.n_entry.grid(row=1, column=1, padx=10, sticky="w", pady=5)
        self.n_entry.insert(0, str(self.n))

        self.steps_label = tk.Label(self.main_frame.canvas, text="Количество этапов (steps):", font=("calibri", 14), anchor='w', bg='#567ec2')
        self.steps_label.grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.steps_entry = tk.Entry(self.main_frame.canvas, validate='key', bg='white', fg='black', font=("calibri", 12))
        self.steps_entry.grid(row=2, column=1, padx=10, sticky="w", pady=5)
        self.steps_entry.insert(0, str(self.steps))

        self.v_label = tk.Label(self.main_frame.canvas, text="Влияние дозировки (v):", font=("calibri", 14), anchor='w', bg='#567ec2')
        self.v_label.grid(row=3, column=0, sticky="w", padx=10, pady=5)
        self.v_entry = tk.Entry(self.main_frame.canvas, validate='key', bg='white', fg='black', font=("calibri", 12))
        self.v_entry.grid(row=3, column=1, padx=10, sticky="w", pady=5)
        self.v_entry.insert(0, str(self.v_range[0]))
        
        self.a_label = tk.Label(self.main_frame.canvas, text="Начальная сахаристость (a):", font=("calibri", 14), anchor='w', bg='#567ec2')
        self.a_label.grid(row=4, column=0, sticky="w", padx=10, pady=5)
        self.a_entry = tk.Entry(self.main_frame.canvas, validate='key', bg='white', fg='black', font=("calibri", 12))
        self.a_entry.grid(row=4, column=1, padx=10, sticky="w", pady=5)
        self.a_entry.insert(0, str(self.a_range[0]))

        self.b_label = tk.Label(self.main_frame.canvas, text="Коэффициент деградации (b):", font=("calibri", 14), anchor='w', bg='#567ec2')
        self.b_label.grid(row=5, column=0, sticky="w", padx=10, pady=5)
        self.b_entry = tk.Entry(self.main_frame.canvas, validate='key', bg='white', fg='black', font=("calibri", 12))
        self.b_entry.grid(row=5, column=1, padx=10, sticky="w", pady=5)
        self.b_entry.insert(0, str(self.b_range[0]))

    def create_checkboxes(self):
        self.inorganic_checkbox_var = tk.BooleanVar()
        self.inorganic_checkbox = tk.Checkbutton(self.main_frame.canvas,
                                                 text="Учитывать неорганические вещества",
                                                 variable=self.inorganic_checkbox_var,
                                                 anchor='w', font=("calibri", 16), relief="ridge", bg='#658BCB')
        self.inorganic_checkbox.grid(row=6, columnspan=2, pady=10)

        self.dosage_checkbox_var = tk.BooleanVar()
        self.dosage_checkbox = tk.Checkbutton(self.main_frame.canvas,
                                              text="Использовать дозаривание",
                                              variable=self.dosage_checkbox_var,
                                              anchor='w', font=("calibri", 16), relief="ridge", bg='#658BCB')
        self.dosage_checkbox.grid(row=7, columnspan=2, pady=10)

    def create_run_button(self):
        self.run_button = tk.Button(self.main_frame.canvas, text="Запустить эксперимент", command=self.on_run_button_click,
                                    bg='#042763', fg='white', anchor='center', font=("calibri", 25), width=20,
                                    height=1, relief="ridge", highlightbackground="white", highlightthickness=1)
        self.run_button.grid(row=9, columnspan=2, pady=20)

    def create_range_labels(self):
        range_label = tk.Label(self.main_frame.canvas,
                               text=f"Интервалы для задания параметров: \n   v ({self.v_range[0]} - {self.v_range[1]}),"
                                    f"a ({self.a_range[0]} - {self.a_range[1]}), "
                                    f"b ({self.b_range[0]} - {self.b_range[1]})",
                               font=("calibri", 14), anchor='w', relief="ridge", bg='#658BCB')
        range_label.grid(row=8, columnspan=2, pady=10)

    def on_run_button_click(self):
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

        results = run_virtual_experiments(self.num_experiments, self.n, self.steps, self.switch_step, self.k,
                                        self.a_range, self.b_range, inorganic_influence, dosage)

        self.update_graph(results)

    def update_graph(self, results):
        plot_results(results)

# Основной запуск
if __name__ == "__main__":
    root = tk.Tk()
    app = ExperimentApp(root)
    root.mainloop()