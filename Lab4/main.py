import argparse
from graph import *
from ratio import *

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Лабораторная работа №4 — Вариант 19 (Pandas & Matplotlib)"
    )
    parser.add_argument(
        "-a",
        "--annotation",
        default="annotation.csv",
        help="Путь к исходному CSV-файлу аннотации (по умолчанию: annotation.csv)",
    )
    parser.add_argument(
        "-o",
        "--output-csv",
        default="enriched_annotation.csv",
        help="Путь для сохранения итогового CSV-файла (по умолчанию: enriched_annotation.csv)",
    )
    parser.add_argument(
        "-p",
        "--output-plot",
        default="zero_samples_histogram.png",
        help="Путь для сохранения файла гистограммы (по умолчанию: zero_samples_histogram.png)",
    )
    parser.add_argument(
        "--min-filter",
        type=float,
        default=0.0,
        help="Минимальный порог фильтрации по 'zero_samples_ratio' (по умолчанию: 0.0)",
    )
    parser.add_argument(
        "--max-filter",
        type=float,
        default=1.0,
        help="Максимальный порог фильтрации по 'zero_samples_ratio' (по умолчанию: 1.0)",
    )

    args = parser.parse_args()

    # 1. Формирование и расширение DataFrame
    df = load_and_enrich_dataframe(args.annotation)

    # 2. Сортировка по добавленной колонке
    sorted_df = sort_by_zero_ratio(df, ascending=True)

    print("\n--- Первые 5 строк отсортированного датафрейма ---")
    print(sorted_df.head())

    # 3. Демонстрация функции фильтрации
    filtered_df = filter_by_zero_ratio(
        sorted_df,
        min_threshold=args.min_filter,
        max_threshold=args.max_filter,
    )

    print(
        f"\nЗаписей после фильтрации (в диапазоне [{args.min_filter}, {args.max_filter}]): {len(filtered_df)}"
    )

    # 4. Сохранение итогового датафрейма в новый CSV
    sorted_df.to_csv(args.output_csv, index=False, encoding="utf-8")
    print(f"\nОбработанный датафрейм сохранен в: {args.output_csv}")

    # 5. Отображение и сохранение гистограммы для ВСЕХ отсортированных данных
    plot_and_save_histogram(sorted_df, args.output_plot)


if __name__ == "__main__":
    main()