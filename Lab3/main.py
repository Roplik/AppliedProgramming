import argparse
import os

import soundfile as sf
from graph import *
from redactAudio import *



def main() -> None:
    """Главная функция: считывает аргументы, выполняет обработку аудио,

    выводит параметры в консоль, визуализирует и сохраняет результат.
    """
    parser = argparse.ArgumentParser(
        description="Лабораторная работа №3 — Вариант 19 (Обработка многомерных массивов / Аудио)"
    )
    parser.add_argument(
        "-i",
        "--input",
        required=True,
        help="Путь к исходному аудиофайлу (например, sound_1.mp3 или .wav)",
    )
    parser.add_argument(
        "-o",
        "--output",
        default="result/processed_sound.wav",
        help="Путь для сохранения результата (по умолчанию: processed_sound.wav)",
    )
    parser.add_argument(
        "-s",
        "--speed",
        type=float,
        default=1.5,
        help="Коэффициент ускорения аудио (по умолчанию: 1.5)",
    )
    parser.add_argument(
        "--second-input",
        default=None,
        help="Путь ко второму аудиофайлу для склейки (если не указан, использует первый)",
    )

    args = parser.parse_args()

    # 1. Считывание первого аудиофайла
    if not os.path.isfile(args.input):
        print(f"[!] Ошибка: Исходный файл '{args.input}' не найден.")
        return

    data, samplerate = sf.read(args.input)

    # 2. Вывод характеристик и размера аудиомассива
    print("\n--- Характеристики исходного файла ---")
    print(f"Путь: {args.input}")
    print(f"Размер массива сэмплов (shape): {data.shape}")
    print(f"Тип данных: {data.dtype}")
    print(f"Частота дискретизации: {samplerate} Hz")
    duration = len(data) / samplerate
    print(f"Длительность: {duration:.2f} сек.")

    # 3. Применение преобразований
    print("\n--- Выполнение преобразований (Вариант 19) ---")

    # Увеличение скорости
    print(f"1. Увеличение скорости в {args.speed} раз...")
    speeded_data = speed_up(data, args.speed)


    # Склейка двух аудиофайлов
    if args.second_input and os.path.isfile(args.second_input):
        print(f"2. Склейка с дополнительным файлом '{args.second_input}'...")
        data2, sr2 = sf.read(args.second_input)
        if sr2 != samplerate:
            print(
                "[!] Предупреждение: Частоты дискретизации файлов различаются!"
            )
    else:
        print("2. Склейка с исходным аудиофайлом...")
        data2 = data

    concatenated_data = concatenate_audio(speeded_data, data2)


    print("3. Усиление высоких частот...")
    final_data = boost_high_frequencies(concatenated_data)

    print(f"Итоговый размер массива: {final_data.shape}")

    # 4. Сохранение результата в файл
    sf.write(args.output, final_data, samplerate)
    print(f"\nРезультат успешно сохранен в: {os.path.abspath(args.output)}")

    # 5. Визуализация графиков с помощью Matplotlib
    plot_audio_signals(data, final_data, samplerate, samplerate)


if __name__ == "__main__":
    main()