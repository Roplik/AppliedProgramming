import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def download_from_link(link: str, save_path: str,name: str, headers: map) -> tuple[str, str] | None:
    """Выполняет HTTP-запрос и сохраняет MP3-файл по указанной ссылке.

    Args:
        link (str): Полный URL-адрес для скачивания аудиофайла.
        save_path (str): Директория, в которую необходимо сохранить файл.
        name (str): Идентификатор файла (используется для формирования имени 'sound_<name>.mp3').
        headers (dict): Заголовки HTTP-запроса (User-Agent и др.).

    Returns:
        tuple[str, str] | None: Кортеж из (относительный путь, абсолютный путь) в случае успешного 
        скачивания, либо None в случае ошибки HTTP-запроса (код ответа != 200).
    """
    filename = os.path.join(save_path, f"sound_{name}.mp3")
    rel_path = filename
    abs_path = os.path.abspath(rel_path)

    
    print(f"Скачиваем: {filename}...")
    
    file_res = requests.get(link, headers=headers)
    if file_res.status_code == 200:
        with open(filename, "wb") as f:
            f.write(file_res.content)
        print(f"Сохранено: {filename}")
        return rel_path, abs_path
    else:
        print(f"Ошибка при скачивании {link}")
        return None



def download_sound(keywords: list[str], outpath: str="result", min_size: int=30, max_size: int=100) -> None:
    """Ищет и скачивает аудиофайлы с сайта sound-effects.ru по ключевым словам.

    Функция последовательно делает запросы к поиску по ключевым словам из списка,
    собирает теги ссылок для скачивания до достижения порога min_size, после чего 
    загружает до max_size файлов на диск.

    Args:
        keywords (list[str]): Список ключевых слов для поиска треков.
        outpath (str, optional): Путь к папке сохранения файлов. По умолчанию "result".
        min_size (int, optional): Минимальное целевое количество найденных ссылок. По умолчанию 30.
        max_size (int, optional): Максимальное количество файлов для загрузки. По умолчанию 100.

    Returns:
        list[tuple[str, str]]: Список кортежей вида (относительный путь, абсолютный путь)
        для всех успешно загруженных файлов.
    """
    download_links:list = []

    keys: list[str] = keywords

    if not (os.path.exists(outpath)):
        os.makedirs(outpath)
        
    actual_keys_index: int = 0


    base_url: str = 'https://sound-effects.ru/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    while(len(download_links) < min_size):
        actual_url: str = base_url
        if len(keys) > 0:
            actual_url += f"?s={keys[actual_keys_index]}"
        print(actual_url)

        response = requests.get(actual_url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        download_links += soup.find_all("a", class_="downloadlink")

        
        

        
        print(f"Найдено файлов для скачивания: {len(download_links)}")

        if len(download_links) < min_size and len(keys) != actual_keys_index:
            actual_keys_index += 1
        
        if len(keys) == actual_keys_index:
            print(f"К сожалению по этим тегам на сайте всего {len(download_links)} результатов. "
                  "Перехожу к скачиванию")
            break
        

    downloaded_records = []
    for i in range(min(len(download_links), max_size)):
        link = download_links[i]
        relative_url = link.get("href")
        if not relative_url:
            continue
        
        full_url = urljoin(base_url, relative_url)
        post_id = link.get("id", "").replace("pld_", "") or relative_url.split("post_id=")[-1]
        paths = download_from_link(full_url, outpath, post_id, headers)
        if paths:
            downloaded_records.append(paths)

    print("Скачивание завершено!")
    return downloaded_records
