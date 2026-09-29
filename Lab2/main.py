import argparse
from annotation import *
from iterator import *
from downloader import *


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Лабораторная работа №2 - Вариант 19")
    parser.add_argument('-k', '--keywords', nargs='+', required=True, help="Ключевые слова для поиска")
    parser.add_argument('-o', '--output', default='result', help="Папка для сохранения")
    parser.add_argument('-a', '--annotation', default='annotation.csv', help="Путь к файлу аннотации CSV")
    parser.add_argument('-n', '--count', type=int, default=30, help="Количество файлов (минимум 30)")

    args = parser.parse_args()

    print(args.keywords)
    records = download_sound(args.keywords, args.output, args.count)

    if records:
        create_annotation_csv(records, args.annotation)

        print("\n--- Демонстрация работы итератора по CSV ---")
        path_iterator = AudioPathIterator(args.annotation)
        for i, path in enumerate(path_iterator, 1):
            print(f"{i}. {path}")