# Price Monitor API

Асинхронный сервис для отслеживания цен криптовалют в реальном времени. Celery автоматически запрашивает цены с CoinGecko API каждую минуту и сохраняет историю изменений.

![Tests](https://github.com/eternal-silence00/Price-Monitor/actions/workflows/tests.yml/badge.svg)

## Стек технологий

- FastAPI — асинхронный веб-фреймворк
- PostgreSQL — основная база данных
- SQLAlchemy — ORM для работы с БД
- Alembic — миграции базы данных
- Redis — кеширование + брокер для Celery
- Celery + Celery Beat — фоновые задачи и планировщик
- JWT — авторизация через токены
- Nginx — reverse proxy
- WebSocket — real-time обновление цен
- fastapi-mail — отправка email уведомлений
- Docker / Docker Compose — контейнеризация
- Pydantic — валидация данных
- pytest — тестирование с тестовой БД
- GitHub Actions — CI/CD

## Функциональность

- Регистрация и авторизация пользователей через JWT
- Добавление и удаление криптовалют для отслеживания
- Автоматический парсинг цен с CoinGecko API каждую минуту через Celery Beat
- Email уведомления при изменении цены более чем на 5%
- Real-time обновление цен через WebSocket
- История цен по каждой монете с пагинацией
- Эндпоинт для получения последней цены монеты
- Кеширование через Redis с автоматической инвалидацией
- Rate limiting на эндпоинты авторизации (5 запросов в минуту)
- Nginx как reverse proxy перед FastAPI
- Автоматический запуск тестов при каждом пуше через GitHub Actions

## Структура проекта

```
price-monitor/
├── .github/
│   └── workflows/
│       └── tests.yml        # CI/CD pipeline
├── app/
│   ├── main.py              # Точка входа, lifespan
│   ├── config.py            # Настройки через pydantic-settings
│   ├── database.py          # Async подключение к БД
│   ├── redis_client.py      # Redis клиент
│   ├── celery_app.py        # Конфигурация Celery
│   ├── tasks.py             # Celery задача для парсинга цен и отправки уведомлений
│   ├── email.py             # Отправка email уведомлений
│   ├── rate_limiter.py      # Rate limiting через Redis
│   ├── models/
│   │   ├── base.py
│   │   ├── user.py
│   │   ├── tracking.py
│   │   └── price_history.py
│   ├── repositories/
│   │   ├── user.py
│   │   ├── tracking.py
│   │   └── price_history.py
│   ├── services/
│   │   └── auth.py
│   ├── routers/
│   │   ├── auth.py
│   │   ├── tracking.py
│   │   ├── price_history.py
│   │   └── websocket.py
│   └── schemas/
│       ├── auth.py
│       ├── tracking.py
│       └── price_history.py
├── migrations/
├── nginx/
│   └── nginx.conf           # Конфигурация reverse proxy + WebSocket
├── tests/
│   ├── conftest.py
│   ├── test_auth.py
│   └── test_tracking.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── .env
```

## Архитектура

```
Интернет -> Nginx:80 -> FastAPI:8000 -> PostgreSQL
                     -> WebSocket    -> Redis
                     Celery Worker   -> CoinGecko API
                                     -> SMTP (email уведомления)
                     Celery Beat     -> (планировщик)
```

## Запуск проекта

### 1. Клонировать репозиторий

```bash
git clone https://github.com/eternal-silence00/Price-Monitor.git
cd Price-Monitor
```

### 2. Создать `.env` файл

```properties
DATABASE_URL=postgresql+asyncpg://postgres:password@db:5432/price_monitor
REDIS_URL=redis://redis:6379
BASE_URL=http://localhost:8000
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_DB=price_monitor
SECRET_KEY=your_secret_key
ALGORITHM=HS256
MAIL_USERNAME=your@gmail.com
MAIL_PASSWORD=your_app_password
MAIL_FROM=your@gmail.com
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
```

### 3. Запустить через Docker

```bash
docker-compose up --build
```

### 4. Применить миграции

```bash
docker-compose exec app alembic upgrade head
```

### 5. Открыть документацию

```
http://localhost/docs
```

## API Endpoints

### Авторизация (rate limit: 5 запросов в минуту)

| Метод | Путь | Описание |
|-------|------|----------|
| POST | /register | Регистрация |
| POST | /login | Вход и получение JWT |

### Отслеживание (требуют JWT)

| Метод | Путь | Описание |
|-------|------|----------|
| GET | /tracking | Список отслеживаемых монет |
| POST | /tracking | Добавить монету |
| GET | /tracking/{id} | Получить трекинг по ID |
| DELETE | /tracking/{id} | Удалить трекинг |

### История цен

| Метод | Путь | Описание |
|-------|------|----------|
| GET | /price_history/{coin_id}/latest | Последняя цена монеты |
| GET | /price_history/{coin_id} | История цен монеты |

### WebSocket

| Протокол | Путь | Описание |
|----------|------|----------|
| WS | /ws/{coin_id} | Real-time обновление цены монеты |

Пример подключения:

```javascript
const ws = new WebSocket("ws://localhost/ws/bitcoin");
ws.onmessage = (event) => console.log(event.data);
```

## CI/CD

При каждом пуше в `main` и при создании Pull Request автоматически запускаются тесты через GitHub Actions. Pipeline поднимает PostgreSQL и Redis, устанавливает зависимости и прогоняет весь тест-сьют.

```bash
# Локальный запуск тестов
docker-compose exec app pytest tests/ -v
```

Тесты используют отдельную БД `pricemonitor_test` и не затрагивают основные данные.

## Архитектурные решения

**Celery Beat** — планировщик запускает задачу `fetch_coin_price` каждые 60 секунд. Воркер получает список всех отслеживаемых монет и запрашивает цены из CoinGecko API.

**WebSocket** — клиент подключается к `ws://localhost/ws/{coin_id}` и получает последнюю цену каждые 60 секунд без необходимости делать HTTP запросы. Nginx настроен для проксирования WebSocket соединений через заголовки Upgrade.

**Email уведомления** — после каждого обновления цены Celery сравнивает новую цену с предыдущей. Если изменение превышает 5% — все пользователи отслеживающие эту монету получают email через Gmail SMTP.

**Rate limiting** — эндпоинты авторизации защищены от брутфорса. Redis хранит счётчик запросов по IP и пути. После 5 запросов в минуту возвращается 429.

**Cache-Aside паттерн** — трекинги и история цен кешируются в Redis. Кеш инвалидируется при добавлении и удалении трекингов.

**Nginx reverse proxy** — принимает все входящие запросы на порту 80 и перенаправляет на FastAPI. Поддерживает WebSocket через заголовки Upgrade/Connection.

**Repository паттерн** — слой репозитория отделяет бизнес-логику от работы с БД.