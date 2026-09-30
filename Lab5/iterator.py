import os
import csv

class AudioPathIterator:
    """Итератор для поочередного получения абсолютных путей к аудиофайлам.

    Поддерживает работу с двумя источниками данных: CSV-файлом аннотации 
    или директорией на диске.

    Attributes:
        paths (list[str]): Список абсолютных путей к файлам.
        index (int): Текущий индекс итерации.
    """

    def __init__(self, target_path: str):
        """Инициализирует итератор и загружает пути к файлам.

        Args:
            target_path (str): Путь к CSV-файлу аннотации (со столбцом 'absolute_path')
                или путь к папке с аудиофайлами.

        Raises:
            ValueError: Если указанный target_path не существует на диске.
        """
        self.paths = []
        self.index = 0

        if os.path.isfile(target_path):
            with open(target_path, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    self.paths.append(row['absolute_path'])
        elif os.path.isdir(target_path):
            for root, _, files in os.walk(target_path):
                for file in files:
                    self.paths.append(os.path.abspath(os.path.join(root, file)))
        else:
            raise ValueError(f"Путь {target_path} не найден.")

    def __iter__(self):
        """Возвращает экземпляр итератора.

        Returns:
            AudioPathIterator: Текущий объект итератора.
        """
        return self

    def __next__(self):
        """Возвращает следующий абсолютный путь к файлу.

        Returns:
            str: Абсолютный путь к очередному аудиофайлу.

        Raises:
            StopIteration: Когда все пути из списка перебраны.
        """
        if self.index < len(self.paths):
            path = self.paths[self.index]
            self.index += 1
            return path
        raise StopIteration