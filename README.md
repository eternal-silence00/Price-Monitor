# Price Monitor API
 
Асинхронный сервис для отслеживания цен криптовалют в реальном времени. Celery автоматически запрашивает цены с CoinGecko API каждую минуту и сохраняет историю изменений.
 
## Стек технологий
 
- FastAPI — асинхронный веб-фреймворк
- PostgreSQL — основная база данных
- SQLAlchemy — ORM для работы с БД
- Alembic — миграции базы данных
- Redis — кеширование + брокер для Celery
- Celery + Celery Beat — фоновые задачи и планировщик
- JWT — авторизация через токены
- Nginx — reverse proxy
- Docker / Docker Compose — контейнеризация
- Pydantic — валидация данных
- pytest — тестирование с тестовой БД
## Функциональность
 
- Регистрация и авторизация пользователей через JWT
- Добавление и удаление криптовалют для отслеживания
- Автоматический парсинг цен с CoinGecko API каждую минуту через Celery Beat
- История цен по каждой монете с пагинацией
- Кеширование через Redis с автоматической инвалидацией
- Nginx как reverse proxy перед FastAPI
## Структура проекта
 
```
price-monitor/
├── app/
│   ├── main.py              # Точка входа, lifespan
│   ├── config.py            # Настройки через pydantic-settings
│   ├── database.py          # Async подключение к БД
│   ├── redis_client.py      # Redis клиент
│   ├── celery_app.py        # Конфигурация Celery
│   ├── tasks.py             # Celery задача для парсинга цен
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
│   │   └── price_history.py
│   └── schemas/
│       ├── auth.py
│       ├── tracking.py
│       └── price_history.py
├── migrations/
├── nginx/
│   └── nginx.conf           # Конфигурация reverse proxy
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
                                     -> Redis
                     Celery Worker   -> CoinGecko API
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
 
### Авторизация
 
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
| GET | /price_history/{coin_id} | История цен монеты |
 
## Запуск тестов
 
```bash
docker-compose exec app pytest tests/ -v
```
 
Тесты используют отдельную БД `pricemonitor_test` и не затрагивают основные данные.
 
## Архитектурные решения
 
**Celery Beat** — планировщик запускает задачу `fetch_coin_price` каждые 60 секунд. Воркер получает список всех отслеживаемых монет и запрашивает цены из CoinGecko API.
 
**Cache-Aside паттерн** — трекинги и история цен кешируются в Redis. Кеш инвалидируется при добавлении и удалении трекингов.
 
**Nginx reverse proxy** — принимает все входящие запросы на порту 80 и перенаправляет на FastAPI. Передаёт реальный IP клиента через заголовки.
 
**Repository паттерн** — слой репозитория отделяет бизнес-логику от работы с БД.