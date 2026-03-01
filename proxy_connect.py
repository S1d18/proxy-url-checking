import requests
import concurrent.futures
import socket
import sys
from requests.exceptions import RequestException
from tqdm import tqdm

# URL для получения списка прокси по умолчанию
DEFAULT_PROXY_URL = 'https://proxy-bunker.com/api2.php'

# URL для проверки через прокси
TEST_URL = 'http://eth0.me'

# Файл для сохранения валидных прокси
OUTPUT_FILE = 'proxy_database.txt'

# Функция для загрузки списка прокси
def load_proxies(proxy_url=DEFAULT_PROXY_URL):
    try:
        print(f"Загрузка прокси с {proxy_url}")
        response = requests.get(proxy_url)
        response.raise_for_status()
        proxy_list = response.text.splitlines()
        return proxy_list
    except RequestException as e:
        print(f"Ошибка загрузки списка прокси: ПРОВЕРЬ ДОСТУПНОСТЬ {proxy_url}")
        return []

# Функция для проверки одной прокси
def check_proxy(proxy, timeout=3):
    proxies = {
        'http': f'socks5://{proxy}',
        'https': f'socks5://{proxy}'
    }
    try:
        # Проверяем соединение с сайтом через прокси
        response = requests.get(TEST_URL, proxies=proxies, timeout=timeout)
        if response.status_code == 200:
            return proxy  # Прокси валидная
    except (RequestException, socket.error):
        pass  # Прокси невалидная
    return None

# Функция для многопоточной проверки прокси с прогресс-баром
def run_proxy_checker(proxies, max_workers=200):
    valid_proxies = []

    # Используем ThreadPoolExecutor для многопоточности
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        # tqdm используется для отображения прогресса
        with tqdm(total=len(proxies), desc="Проверка прокси") as pbar:
            future_to_proxy = {executor.submit(check_proxy, proxy): proxy for proxy in proxies}

            for future in concurrent.futures.as_completed(future_to_proxy):
                proxy = future_to_proxy[future]
                try:
                    result = future.result()
                    if result:
                        valid_proxies.append(result)
                except Exception as e:
                    print(f"Ошибка при проверке прокси {proxy}: {e}")
                finally:
                    pbar.update(1)  # Обновляем прогресс-бар

    return valid_proxies

# Функция для сохранения валидных прокси в файл (пересоздание файла)
def save_valid_proxies(valid_proxies):
    if not valid_proxies:
        print("Нет валидных прокси для сохранения.")
        return

    # Открываем файл в режиме 'w' (перезаписываем его)
    with open(OUTPUT_FILE, 'w') as f:
        for proxy in valid_proxies:
            f.write(proxy + '\n')
    print(f"Валидные прокси сохранены в {OUTPUT_FILE}")
    print(f"Всего валидных прокси: {len(valid_proxies)}")  # Выводим количество валидных прокси

# Основная функция
def main():
    # Если передан аргумент, используем его как URL для загрузки прокси
    if len(sys.argv) > 1:
        proxy_url = sys.argv[1]
    else:
        proxy_url = DEFAULT_PROXY_URL

    # Загружаем список прокси
    proxies = load_proxies(proxy_url)
    if not proxies:
        print("Список прокси пуст или не удалось его загрузить.")
        return

    # Запускаем многопоточную проверку
    print(f"Начинаем проверку {len(proxies)} прокси...")
    valid_proxies = run_proxy_checker(proxies)

    # Сохраняем валидные прокси и выводим их количество
    save_valid_proxies(valid_proxies)

if __name__ == "__main__":
    main()
