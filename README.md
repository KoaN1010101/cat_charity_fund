# QRKot

Фонд собирает пожертвования на различные целевые проекты: на медицинское обслуживание нуждающихся хвостатых, на обустройство кошачьей колонии в подвале, на корм оставшимся без попечения кошкам — на любые цели, связанные с поддержкой кошачьей популяции.

# Технологии:
- Python 3.9
- FastAPI
- SQLAlchemy
- Alembic

# Установка
## Склонируйте репозиторий:
```
git clone git@github.com:KoaN1010101/cat_charity_fund.git
```
## Активируйте venv и установите зависимости:
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
## Создайте в корневой директории файл .env со следующим наполнением:
```
APP_TITLE=<ваше название приложения>
DATABASE_URL=<настройки подключения к БД, например: sqlite+aiosqlite:///./development.db>
SECRET=<секретный ключ>
```
# Управление:

## Выполнить миграции
```
alembic upgrade head
```
## Запустить приложение
```
uvicorn app.main:app --reload
```

# Автор
[Никулин Владимир](https://github.com/KoaN1010101)


# Документация к API:

Swagger: http://127.0.0.1:8000/docs
Redoc: http://127.0.0.1:8000/redoc