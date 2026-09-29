import csv
import os
def create_annotation_csv(records: list[tuple[str, str]], annotation_path: str) -> None:
    """Записывает информацию о скачанных файлах в CSV-файл аннотации.

    Создает таблицу с заголовками 'relative_path' и 'absolute_path'.
    Если папка назначения не существует, функция создает ее автоматически.

    Args:
        records (list[tuple[str, str]]): Список кортежей с путями к файлам
            вида (relative_path, absolute_path).
        annotation_path (str): Путь к создаваемому CSV-файлу.

    Returns:
        None
    """
    csv_dir = os.path.dirname(annotation_path)
    if csv_dir:
        os.makedirs(csv_dir, exist_ok=True)

    with open(annotation_path, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['relative_path', 'absolute_path'])
        for rel_p, abs_p in records:
            writer.writerow([rel_p, abs_p])

    print(f"Аннотация успешно создана: {annotation_path}")