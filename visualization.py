import matplotlib.pyplot as plt

def plot_results(results):
    """
    Функция для отображения результатов эксперимента с графиком сравнения стратегий.
    """
    best_strategy = max(results.items(), key=lambda x: x[1]['sugar'])[0]
    recommendation_text = f"Рекомендуемая стратегия: {best_strategy}\n"
    recommendation_text += f"Выход сахара: {results[best_strategy]['sugar']:.2f}\n"
    recommendation_text += f"Потери сахара: {results[best_strategy]['losses']:.2f}"

    strategies = list(results.keys())
    sugar_values = [results[strategy]['sugar'] for strategy in strategies]
    losses_values = [results[strategy]['losses'] for strategy in strategies]

    x = range(len(strategies))

    # Создаём график
    plt.figure(figsize=(10, 6))  # Размер графика

    # Построение графиков
    plt.bar(x, sugar_values, width=0.4, label="Выход сахара", align='center', color='blue')
    plt.bar(x, losses_values, width=0.4, label="Относительные потери", align='edge', color='red')

    # Настройки графика
    plt.xlabel("Стратегия")
    plt.ylabel("Значение")
    plt.title("Сравнение стратегий по выходу сахара и потерям")
    plt.xticks(x, strategies, rotation=45)
    plt.legend()
    plt.grid(axis='y')

    # Добавление текста с рекомендацией
    plt.text(
        0.95, 0.95, recommendation_text,
        transform=plt.gca().transAxes,
        fontsize=10, verticalalignment='top', horizontalalignment='right',
        bbox=dict(facecolor='white', alpha=0.8, edgecolor='black')
    )

    # Применяем улучшения для плотного расположения элементов
    plt.tight_layout()

    # Отображаем график
    plt.show()