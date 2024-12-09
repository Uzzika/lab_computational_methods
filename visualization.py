import matplotlib.pyplot as plt

def plot_results(results):
    best_strategy = max(results.items(), key=lambda x: x[1]['sugar'])[0]
    recommendation_text = f"Recommended Strategy: {best_strategy}\n"
    recommendation_text += f"Sugar Yield: {results[best_strategy]['sugar']:.2f}\n"
    recommendation_text += f"Sugar Losses: {results[best_strategy]['losses']:.2f}"

    strategies = list(results.keys())
    sugar_values = [results[strategy]['sugar'] for strategy in strategies]
    losses_values = [results[strategy]['losses'] for strategy in strategies]

    x = range(len(strategies))
    plt.figure(figsize=(10, 6))

    plt.bar(x, sugar_values, width=0.4, label="Sugar Yield", align='center', color='#FFA400')
    plt.bar(x, losses_values, width=0.4, label="Relative Losses", align='edge', color='#1049A9')

    plt.xlabel("Strategy")
    plt.ylabel("Value")
    plt.title("Comparison of Strategies by Sugar Yield and Losses")
    plt.xticks(x, strategies, rotation=45)
    plt.legend()
    plt.grid(axis='y')

    plt.text(
        0.15, 0.95, recommendation_text,
        transform=plt.gca().transAxes,
        fontsize=10,
        verticalalignment='top',
        horizontalalignment='left',
        bbox=dict(facecolor='white', alpha=0.8, edgecolor='black')
    )

    plt.tight_layout()
    plt.show()