# Baseline of AI Assistant Hack: Python

По вопросам/багам писать в tg: [@werserk](https://t.me/werserk)

## Ссылки

Репозиторий: https://github.com/werserk/hse-aiahp-baseline \
Тестирующая система: https://dsworks.ru/champ/hse-2024-october \
Лендинг: https://www.hse.ru/ai-assistant-hack-python/

## Описание

В бейзлайне использована бесплатная версия модели YandexGPT.

## Запуск

### В контейнере

```bash
docker compose up
```

### В локальной среде

```bash
poetry install
```

### Переменные окружения

Создали для вас .env.example файл в корне проекта. \
Чтобы создать .env файл, запускаем следующую команду:

```bash
cp .env.example .env
```

Как получить IAM Token и Folder ID можно посмотреть в [документации](https://yandex.cloud/en-ru/docs/foundation-models/quickstart/yandexgpt#api_2) Yandex Cloud.

Но ещё раз упомянем, что вы в праве выбрать любую модель за исключением платных и недоступных в РФ.

## Структура проекта

```
.
├── app
│   ├── __init__.py
│   └── models
│       ├── __init__.py
│       └── yandexgpt.py
├── data
│   ├── complete
│   ├── processed
│   └── raw
├── main.py
├── notebooks
├── poetry.lock
├── pyproject.toml
└── README.md

```