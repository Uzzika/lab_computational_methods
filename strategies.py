import random
import numpy as np
from scipy.optimize import linear_sum_assignment

def generate_data_with_dosage(n, steps, a_range, b_range, inorganic_influence=False, dosage=False):
    """
    Генерация данных для эксперимента с учетом дозаривания и неорганических веществ.
    """
    if a_range[0] < 0 or a_range[1] <= a_range[0]:
        raise ValueError("Некорректный диапазон a_range.")
    if b_range[0] < 0 or b_range[1] <= b_range[0]:
        raise ValueError("Некорректный диапазон b_range.")

    s_matrix = [[random.uniform(*a_range) for _ in range(steps)] for _ in range(n)]  # сахаристость
    b_matrix = [[random.uniform(*b_range) for _ in range(steps)] for _ in range(n)]  # коэффициенты деградации

    inorganic_params = []
    if inorganic_influence:
        # Генерация параметров для K, Na, N
        inorganic_params = [
            {
                'K': random.uniform(4.8, 7.05),
                'Na': random.uniform(0.21, 0.82),
                'N': random.uniform(1.58, 2.8),
            }
            for _ in range(n)
        ]

    if dosage:
        # Если дозаривание учитывается, изменяем коэффициенты деградации
        for i in range(n):
            for j in range(steps):
                b_matrix[i][j] = random.uniform(0.85, 1.15)  # Допустимые значения дозаривания для b

    return s_matrix, b_matrix, inorganic_params

def calculate_I_values(n, steps, I0_range=(0.62, 0.64)):
    I0 = [random.uniform(*I0_range) for _ in range(n)]  # Генерация значений I0
    I_matrix = [
        [round(I0[i] * (1.029 - j * 0.029), 4) for j in range(steps)] for i in range(n)
    ]  # Вычисление значений I_ij
    return I0, I_matrix

def calculate_matrices(s_matrix, b_matrix, I_matrix, inorganic_influence, inorganic_params=None):
    n = len(s_matrix)
    steps = len(s_matrix[0])

    C = [[0] * steps for _ in range(n)]
    L = [[0] * steps for _ in range(n)]
    S = [[0] * steps for _ in range(n)]

    for i in range(n):
        for j in range(steps):
            C[i][j] = s_matrix[i][j] * b_matrix[i][j]  # Сахаристость с учетом деградации

            if inorganic_influence and inorganic_params:
                params = inorganic_params[i]
                potential_loss = 0.5 * (params['K'] + params['Na'] + params['N'])  # Потери из-за неорганических веществ
                L[i][j] = min(potential_loss, 0.3 * C[i][j])  # Ограничение потерь
            else:
                L[i][j] = 0

            L[i][j] = min(L[i][j], C[i][j])  # Ограничение потерь по сахару
            S[i][j] = max(0, C[i][j] - L[i][j])  # Оставшийся сахар

    return C, L, S

def run_experiment(n, steps, switch_step, k, s_matrix, b_matrix, inorganic_influence, inorganic_params):
    """
    Запуск эксперимента для каждой стратегии.
    """
    strategies = {
        "Greedy": lambda b, s, cs: max(b, key=lambda batch: s[batch][cs] if s[batch][cs] > 0 else -1),
        "Thrifty": lambda b, s, cs: min(b, key=lambda batch: s[batch][cs] if s[batch][cs] > 0 else float('inf')),
        "Thrifty/Greedy": lambda b, s, cs: min(b, key=lambda batch: s[batch][cs] if s[batch][cs] > 0 else float('inf')) if cs < switch_step else max(b, key=lambda batch: s[batch][cs] if s[batch][cs] > 0 else -1),
        "Greedy/Thrifty": lambda b, s, cs: max(b, key=lambda batch: s[batch][cs] if s[batch][cs] > 0 else -1) if cs < switch_step else min(b, key=lambda batch: s[batch][cs] if s[batch][cs] > 0 else float('inf')),
        "T(k)G": lambda b, s, cs: sorted(b, key=lambda batch: s[batch][cs])[min(k-1, len(b)-1)] if cs < switch_step else max(b, key=lambda batch: s[batch][cs]),
        "CTG": lambda b, s, cs: min(b, key=lambda batch: s[batch][cs]),
        "Balanced": lambda b, s, cs: max(b, key=lambda batch: s[batch][cs] - 0.5 * b_matrix[batch][cs] if s[batch][cs] > 0 else -1),
    }

    results = {name: {'sugar': 0, 'losses': 0} for name in strategies}

    for name, strategy in strategies.items():
        total_sugar = 0
        total_losses = 0
        batches = list(range(n))

        for step in range(steps):
            if not batches:
                break

            # Применение стратегии
            selected_batch = strategy(batches, s_matrix, step)

            sugar = s_matrix[selected_batch][step]
            degradation = b_matrix[selected_batch][step]

            # Вычисление потерь
            loss = sugar * max(0, 1 - degradation)

            # Суммирование результата
            total_sugar += sugar
            total_losses += loss

            # Удаление обработанной партии
            batches.remove(selected_batch)

        results[name] = {'sugar': total_sugar, 'losses': total_losses}

    return results

def run_virtual_experiments(num_experiments, n, steps, switch_step, k, a_range, b_range, inorganic_influence=False, dosage=False):
    """
    Проведение виртуальных экспериментов для оценки стратегий.
    """
    total_results = {
        name: {'sugar': 0, 'losses': 0}
        for name in ["Greedy", "Thrifty", "Thrifty/Greedy", "Greedy/Thrifty", "T(k)G", "CTG", "Balanced"]
    }

    for _ in range(num_experiments):
        s_matrix, b_matrix, inorganic_params = generate_data_with_dosage(n, steps, a_range, b_range, inorganic_influence, dosage)
        _, I_matrix = calculate_I_values(n, steps)
        _, _, S = calculate_matrices(s_matrix, b_matrix, I_matrix, inorganic_influence, inorganic_params)

        experiment_results = run_experiment(n, steps, switch_step, k, S, b_matrix, inorganic_influence, inorganic_params)
        for strategy, value in experiment_results.items():
            total_results[strategy]['sugar'] += value['sugar']
            total_results[strategy]['losses'] += value['losses']

    # Усреднение результатов
    for strategy in total_results:
        total_results[strategy]['sugar'] /= num_experiments
        total_results[strategy]['losses'] /= num_experiments

    return total_results