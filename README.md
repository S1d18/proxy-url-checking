# Proxy URL Checking
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

Утилита для проверки и фильтрации SOCKS5 прокси.

## Возможности

- Загрузка прокси-листов из публичных источников
- Многопоточная валидация (до 200 потоков)
- Проверка SOCKS5 прокси
- Прогресс-бар (tqdm)
- Поддержка пользовательского URL через аргументы командной строки
- Сохранение рабочих прокси в файл

## Технологии

- Python 3
- requests + PySocks
- concurrent.futures (ThreadPoolExecutor)
- tqdm

## Установка

```bash
git clone https://github.com/<username>/proxy-url-checking.git
cd proxy-url-checking
pip install requests pysocks tqdm
```

## Использование

### С URL по умолчанию
```bash
python proxy_connect.py
```

### С пользовательским URL
```bash
python proxy_connect.py "https://example.com/proxy-list"
```

### Базовая версия
```bash
python proxy_manager.py
```

Результаты сохраняются в `proxy_database.txt`.
