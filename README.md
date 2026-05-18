# Price Monitor API
 
Асинхронный сервис для отслеживания цен криптовалют в реальном времени. Celery автоматически получает актуальные цены с CoinGecko API каждую минуту и сохраняет историю изменений.
 
## Стек технологий
 
- FastAPI — асинхронный веб-фреймворк
- PostgreSQL — основная база данных
- SQLAlchemy — ORM для работы с БД
- Alembic — миграции базы данных
- Redis — кеширование данных (Cache-Aside паттерн)
- Celery + Celery Beat — фоновые задачи и планировщик
- CoinGecko API — источник цен криптовалют
- JWT — авторизация через токены
- Docker / Docker Compose — контейнеризация
- Pydantic — валидация данных
- pytest — тестирование с тестовой БД
## Функциональность
 
- Регистрация и авторизация пользователей через JWT
- Добавление и удаление отслеживаемых криптовалют
- Автоматический парсинг цен каждую минуту через Celery Beat
- История цен по каждой монете с пагинацией
- Кеширование через Redis с автоматической инвалидацией
- Тесты с отдельной тестовой БД
## Структура проекта
 
```
price-monitor/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── redis_client.py
│   ├── celery_app.py
│   ├── tasks.py
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
├── tests/
│   ├── conftest.py
│   ├── test_auth.py
│   └── test_tracking.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── .env
```
 
## Запуск проекта
 
### 1. Клонировать репозиторий
 
```bash
git clone https://github.com/eternal-silence00/Price-Monitor.git
cd Price-Monitor
```
 
### 2. Создать .env файл
 
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
http://localhost:8000/docs
```
 
## API Endpoints
 
### Авторизация
 
| Метод | Путь | Описание |
|-------|------|----------|
| POST | /register | Регистрация пользователя |
| POST | /login | Вход и получение JWT токена |
 
### Отслеживание (требуют JWT токен)
 
| Метод | Путь | Описание |
|-------|------|----------|
| GET | /tracking | Получить все отслеживаемые монеты |
| GET | /tracking/{tracking_id} | Получить отслеживание по ID |
| POST | /tracking | Добавить монету для отслеживания |
| DELETE | /tracking/{tracking_id} | Удалить отслеживание |
 
### История цен
 
| Метод | Путь | Описание |
|-------|------|----------|
| GET | /price_history/{coin_id} | История цен монеты |
 
## Архитектурные решения
 
JWT авторизация — stateless аутентификация. Каждый запрос содержит токен с user_id. Сервер не хранит сессии.
 
Cache-Aside паттерн — при запросе данных сначала проверяется Redis. Кеш инвалидируется при создании и удалении трекингов.
 
Celery Beat — планировщик запускает задачу парсинга каждые 60 секунд. Цены хранятся в таблице price_history и доступны всем пользователям — без дублирования данных.
 
Repository паттерн — слой репозитория отделяет бизнес-логику от работы с БД.
 
## Запуск тестов
 
```bash
docker-compose exec app pytest tests/ -v
```
 
Тесты используют отдельную БД pricemonitor_test и не затрагивают основные данные.