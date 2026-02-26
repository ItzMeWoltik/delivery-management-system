# Delivery Management System

Повностековий пет-проєкт системи доставки їжі/товарів для демонстрації навичок.

### Основні можливості

- Реєстрація та авторизація (клієнт / кур'єр / адмін / підтримка)
- JWT + refresh-токени, ролевий доступ
- Створення, відстеження, скасування та оплата замовлень (мок Stripe)
- Реальний час чат клієнт ↔ кур'єр та підтримка (WebSocket)
- Жива геолокація кур'єрів + виявлення фейкового GPS (швидкість, телепортація)
- Прогресивна система пауз для кур'єрів замість штрафів
- Адмін-панель: дашборд, алерти, управління замовленнями, рефанди, гео-історія
- Двомовність: українська + англійська (перемикання через API)
- Docker + PostgreSQL + Alembic міграції + тести (Pytest + Jest)

### Технології

**Бекенд**  
- Python 3.10  
- FastAPI  
- SQLAlchemy + Alembic  
- PostgreSQL  
- PyJWT, Requests, WebSocket  

**Фронтенд**  
- React 18  
- React Router  
- Axios  
- WebSocket  
- Context API для авторизації  
- i18n (переклади)  

**Інфраструктура**  
- Docker + Docker Compose  
- Swagger для документації API  

### Як запустити

1. Клонувати репозиторій
2. У корені виконати:
docker-compose up --build
3. Фронтенд → http://localhost:3000  
API + Swagger → http://localhost:8000/docs  
База даних → PostgreSQL (user: user, pass: pass)

### Демо-користувачі (після seed.py)

- admin@example.com / admin → адмін  
- customer@example.com / pass → клієнт  
- courier@example.com / pass → кур'єр  


Питання/покращення — welcome в issues або pull requests!
