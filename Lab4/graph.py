import os
import matplotlib.pyplot as plt
import pandas as pd


def plot_and_save_histogram(
    sorted_df: pd.DataFrame, output_plot_path: str
) -> None:
    """Строит и сохраняет гистограмму распределения доли нулевых сэмплов для всех

    отсортированных данных.

    Args:
        sorted_df (pd.DataFrame): Отсортированный датафрейм.
        output_plot_path (str): Путь для сохранения графика в файл (например, .png).
    """
    plt.figure(figsize=(10, 6))

    # Построение гистограммы
    plt.hist(
    sorted_df["zero_samples_ratio"],
    bins=15,
    range=(0, 1),
    color="skyblue",
    edgecolor="black",
    alpha=0.7,
    )
    plt.xlim(0, 1)

    # Подписи и оформление
    plt.title(
        "Распределение доли нулевых сэмплов в аудиофайлах (Вариант 19)",
        fontsize=14,
    )
    plt.xlabel("Отношение количества нулевых сэмплов к общему числу", fontsize=12)
    plt.ylabel("Количество аудиофайлов", fontsize=12)
    plt.grid(axis="y", linestyle="--", alpha=0.7)

    # Сохранение графика
    plot_dir = os.path.dirname(output_plot_path)
    if plot_dir:
        os.makedirs(plot_dir, exist_ok=True)

    plt.tight_layout()
    plt.savefig(output_plot_path, dpi=300)
    print(f"График гистограммы успешно сохранен: {output_plot_path}")
    plt.show()
