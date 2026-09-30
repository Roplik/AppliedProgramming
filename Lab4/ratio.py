import os
import numpy as np
import pandas as pd
import soundfile as sf


def calculate_zero_ratio(file_path: str, threshold: float = 0.001) -> float:
    """Вычисляет отношение количества нулевых (тихих) сэмплов к общему количеству сэмплов в аудиофайле.

    Из-за наличия фонового шума и специфики сжатия абсолютные нули в файлах
    практически отсутствуют. Поэтому к категории "нулевых" относятся сэмплы,
    амплитуда которых по модулю ниже заданного порога threshold.

    Args:
        file_path (str): Путь к аудиофайлу.
        threshold (float, optional): Порог амплитуды, ниже которого сэмпл
            считается нулевым (тишиной). По умолчанию равен 0.001.

    Returns:
        float: Доля близких к нулю сэмплов (значение от 0.0 до 1.0).
    """
    try:
        data, _ = sf.read(file_path)
        total_samples = data.size
        if total_samples == 0:
            return 0.0

        zero_samples = np.count_nonzero(np.abs(data) < threshold)

        return float(zero_samples / total_samples)
    except Exception as e:
        print(f"[!] Ошибка при обработке файла '{file_path}': {e}")
        return 0.0


def load_and_enrich_dataframe(csv_annotation_path: str) -> pd.DataFrame:
    """Загружает CSV-аннотацию, задает понятные имена колонок и добавляет колонку

    Args:
        csv_annotation_path (str): Путь к исходному CSV-файлу аннотации.

    Returns:
        pd.DataFrame: Датафрейм с именованными колонками и рассчитанным
        метрическим значением.
    """
    if not os.path.isfile(csv_annotation_path):
        raise FileNotFoundError(
            f"Файл аннотации '{csv_annotation_path}' не найден."
        )

    # 1. Загрузка DataFrame
    df = pd.read_csv(csv_annotation_path)

    # 2. Именование колонок
    if len(df.columns) >= 2:
        df.columns = ["relative_path", "absolute_path"] + list(df.columns[2:])
    else:
        raise ValueError(
            "CSV-файл должен содержать как минимум 2 колонки (относительный и абсолютный пути)."
        )

    print(f"Загружено записей из аннотации: {len(df)}")

    print("Расчет доли нулевых сэмплов для каждого аудиофайла...")
    df["zero_samples_ratio"] = df["absolute_path"].apply(calculate_zero_ratio)

    return df


def sort_by_zero_ratio(
    df: pd.DataFrame, ascending: bool = True
) -> pd.DataFrame:
    """Сортирует DataFrame по колонке 'zero_samples_ratio'.

    Args:
        df (pd.DataFrame): Исходный датафрейм.
        ascending (bool, optional): Флаг порядка сортировки (по возрастанию/убыванию).
            По умолчанию True.

    Returns:
        pd.DataFrame: Отсортированный датафрейм.
    """
    return df.sort_values(
        by="zero_samples_ratio", ascending=ascending
    ).reset_index(drop=True)


def filter_by_zero_ratio(
    df: pd.DataFrame, min_threshold: float = 0.0, max_threshold: float = 1.0
) -> pd.DataFrame:
    """Фильтрует DataFrame по диапазону значений 'zero_samples_ratio'.

    Args:
        df (pd.DataFrame): Исходный датафрейм.
        min_threshold (float, optional): Минимальная доля нулевых сэмплов.
            По умолчанию 0.0.
        max_threshold (float, optional): Максимальная доля нулевых сэмплов.
            По умолчанию 1.0.

    Returns:
        pd.DataFrame: Отфильтрованный датафрейм.
    """
    filtered_df = df[
        (df["zero_samples_ratio"] >= min_threshold)
        & (df["zero_samples_ratio"] <= max_threshold)
    ]
    return filtered_df.reset_index(drop=True)