import argparse
import re


def parse_profiles(filename: str) -> list[list[str]]:
    """
    Считывает и группирует анкеты из текстового файла.
    
    Автоматически очищает префиксы типа "Фамилия: ", "1)" и т.д.

    :param filename: Путь к файлу с данными.
    :return: Список анкет, где каждая анкета состоит из 6 значений.
    :raises FileNotFoundError: Если файл не найден.
    """
    profiles: list[list[str]] = []

    with open(filename, 'r', encoding='utf-8') as file:
        raw_lines: list[str] = [line.strip() for line in file if line.strip()]

    clean_lines: list[str] = []
    for line in raw_lines:
        if re.match(r'^\d+\)$', line):
            continue

        cleaned: str = re.sub(
            r'^(Фамилия|Имя|Пол|Дата рождения|Номер телефона или email|Город):\s*',
            '',
            line,
            flags=re.IGNORECASE,
        )
        clean_lines.append(cleaned)

    for i in range(0, len(clean_lines), 6):
        profile_lines: list[str] = clean_lines[i : i + 6]
        if len(profile_lines) == 6:
            profiles.append(profile_lines)

    return profiles


def is_valid_email(email_str: str) -> bool:
    """
    Проверяет корректность формата email.
    """
    pattern: str = r'^[A-Za-z0-9._%+-]{1,64}@(gmail\.com|mail\.ru|yandex\.ru)$'
    return bool(re.match(pattern, email_str))


def is_email_attempt(contact_str: str) -> bool:
    """
    Определяет, является ли строка попыткой ввода email 
    (а не телефона или чего-то другого).
    
    Признаки email:
    - Содержит символ '@'
    - ИЛИ содержит буквы латинского алфавита (A-Z, a-z)
    """
    return bool(re.search(r'[@a-zA-Z]', contact_str))


def print_invalid_profiles(invalid_profiles: list[list[str]]) -> None:
    """
    Выводит на экран анкеты с некорректным форматом email.

    :param invalid_profiles: Список анкет с невалидными адресами почты.
    """
    print(
        f"--- Найдено анкет с некорректным форматом email: {len(invalid_profiles)} ---\n"
    )
    for idx, profile in enumerate(invalid_profiles, start=1):
        print(f"Анкета #{idx}:")
        print(f"  Фамилия:       {profile[0]}")
        print(f"  Имя:           {profile[1]}")
        print(f"  Пол:           {profile[2]}")
        print(f"  Дата рождения: {profile[3]}")
        print(f"  Email:         {profile[4]}")
        print(f"  Город:         {profile[5]}")
        print("-" * 40)


def save_profiles_to_file(profiles: list[list[str]], output_filename: str) -> None:
    """
    Сохраняет оставшиеся валидные анкеты в новый файл.

    :param profiles: Список сохраненных анкет.
    :param output_filename: Имя файла для записи.
    """
    with open(output_filename, 'w', encoding='utf-8') as file:
        for profile in profiles:
            for line in profile:
                file.write(f"{line}\n")


def process_profiles(
    profiles: list[list[str]],
) -> tuple[list[list[str]], list[list[str]]]:
    """
    Разделяет анкеты на корректные и содержащие некорректную почту.

    :param profiles: Список анкет.
    :return: Кортеж (невалидные_почты, остальные_анкеты).
    """
    invalid_email_profiles: list[list[str]] = []
    valid_profiles: list[list[str]] = []

    for profile in profiles:
        contact: str = profile[4]

        # Если строка похожа на email (есть буквы/символ @)
        if is_email_attempt(contact):
            if is_valid_email(contact):
                valid_profiles.append(profile)
            else:
                # Это почта, но у нее некорректный формат
                invalid_email_profiles.append(profile)
        else:
            # Если букв и '@' нет — значит это номер телефона (валидный или невалидный)
            # Его мы в Варианте 19 НЕ трогаем и не удаляем
            valid_profiles.append(profile)

    return invalid_email_profiles, valid_profiles


def main() -> None:
    """
    Главная функция программы.
    """
    parser = argparse.ArgumentParser(
        description="Лабораторная работа №1. Вариант 19"
    )
    parser.add_argument(
        "filename", type=str, help="Путь к файлу с данными"
    )
    args = parser.parse_args()

    try:
        profiles: list[list[str]] = parse_profiles(args.filename)
        invalid_profiles, valid_profiles = process_profiles(profiles)

        print_invalid_profiles(invalid_profiles)

        output_filename: str = "cleaned_data.txt"
        save_profiles_to_file(valid_profiles, output_filename)

        print(f"\nАнкеты с некорректным email удалены.")
        print(f"Результат сохранен в файл: {output_filename}")

    except FileNotFoundError:
        print(f"Ошибка: Файл '{args.filename}' не найден.")
    except Exception as exc:
        print(f"Произошла ошибка: {exc}")


if __name__ == "__main__":
    main()