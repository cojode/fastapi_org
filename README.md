# fastapi_org

## Запуск:

```bash
cp .env.example .env

docker compose up -d # запускает БД, мигратор проводит миграции, запускается приложение

docker compose -f docker-compose.yml -f deploy/docker-compose.dev.yml --project-directory . up --build # запуск с hot-reload

docker compose run --build --rm api pytest -vv . # запуск тестов

docker compose run --build --rm migrator alembic revision -m "new_revision" # создает новую alembic revision (или любая другая команда alembic)
```

Приложение в начальной конфигурации будет доступно на `localhost:8000`

## Структура

```bash
fastapi_org
├── db                  # DB приложения
│   ├── base.py         # Base-класс моделей
│   ├── dependencies.py # DB зависимости
│   ├── meta.py         # Мета моделей
│   ├── migrations      # Alembic-миграции
│   ├── models          # Модели
│   ├── repos           # Репозитории
│   └── utils.py        # Утилиты
├── dependency.py       # Глобальные зависимости
├── domain              # Сущности домена приложения
│   ├── building.py
│   ├── location.py
│   └── organization.py
├── exceptions.py       # Глобальные исключения
├── __init__.py 
├── log.py              # loguru 
├── __main__.py
├── services            # use-case (сервисный слой)
│   ├── base.py
│   ├── building
│   ├── __init__.py
│   └── organization
├── settings.py         # Конфиг проекта
├── static             
├── __version__.py
└── web                 # Веб приложения
    ├── api             # Роутеры, views и схемы эндпоинтов
    ├── application.py  # Инициализация fastapi
    ├── __init__.py
    └── lifespan.py     # lifespan fastapi app
```


Тестовые данные заполняются в одной из ревизий: `fastapi_org/db/migrations/versions/`

## Эндпоинты:

- `/api/org` - Поиск организаций

- `/api/org/{id}` - Получение организации по id

- `/api/building` - Поиск зданий

Подробнее про эндпоинты в документациях: 

- `/api/docs` - Swagger-документация

- `/api/redoc` - Redoc-документация