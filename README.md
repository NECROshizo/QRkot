# Проект QRKot
## Технологии
[![Python](https://img.shields.io/badge/Python-9?style=flat&logo=Python&logoColor=56C0C0&color=gray)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/-FastAPI-1?style=flat&logo=fastapi&logoColor=56C0C0&color=gray)](https://fastapi.tiangolo.com/)
[![Pydantic](https://img.shields.io/badge/-Pydantic-464646?style=flat&logo=Pydantic&logoColor=56C0C0&color=gray)](https://docs.pydantic.dev/latest/)
[![SQLAlchemy](https://img.shields.io/badge/-SQLAlchemy-464646?style=flat&logo=SQLy&logoColor=56C0C0&color=gray)](https://www.sqlalchemy.org/)
[![Alembic](https://img.shields.io/badge/-Alembic-464646?style=flat&logo=alembic&logoColor=56C0C0&color=gray)](https://alembic.sqlalchemy.org/en/latest/)
[![Uvicorn](https://img.shields.io/badge/-Uvicorn-464646?style=flat&logo=uvicorn&logoColor=56C0C0&color=gray)](https://www.uvicorn.org/)
[![Google Sheets](https://img.shields.io/badge/-GoogleSheets-464646?style=flat&logo=GoogleSheets&logoColor=56C0C0&color=gray)](https://www.google.ru/intl/ru/sheets/about/)

##### Полный список модулей, используемых в проекте, доступен в [requirements.txt](https://github.com/NECROshizo/QRkot_spreadsheets/blob/master/requirements.txt)
## Линтеры
[![Flake8](https://img.shields.io/badge/-flake8-464646?style=flat&logo=flake8&logoColor=56C0C0&color=gray)](https://flake8.pycqa.org/)
## Описание проекта
**QRKot** — это фонд собирающий пожертвования на различные целевые проекты: на медицинское обслуживание нуждающихся хвостатых, на обустройство кошачьей колонии в подвале, на корм оставшимся без попечения кошкам — на любые цели, связанные с поддержкой кошачьей популяции.

#### Реализовано:
- регистрация пользователей
- возможность вносить пожертвования которые распределяются на проекты по прицепу  First In, First Out
- возможности вносить фдминистратору изменения в проекты с определенными ограничениями
- формирования отчета в Google таблицах со списком закрытых проектов отсортированных по скорости закрытия. 
Просмотреть все запросы в формате OpenApi можно посмотреть по адрессу <адресс>/docs
## Установка и настройки
#### Клонировать репозиторий:
``` bash
git clone git@github.com:NECROshizo/cat_charity_fund.git
cd cat_charity_fund
```
#### Создание виртуального окружения:
``` bash
python -m venv venv
```
#### Запуск виртуального окружения:
``` bash
source venv/Scripts/activate - команда для Windows
source venv/bin/activate - команда для Linux и macOS
```
#### Установка зависимостей:
```
python -m pip install --upgrade pip
pip install -r requirements.txt
```
#### Настройка параметров допуска окружения к базе данных
``` bash
touch .env
```
Шаблон файла **.env**
``` bash
APP_TITLE=<Название проекта>
DESCRIPTION=<Описание проекта>
DATABASE_URI=<Расположение и тип базы данных>
SECRET_KEY=<Секретный ключ>
TYPE=service_account
PROJECT_ID=<ID проекта>
PRIVATE_KEY_ID=<ID приватного ключа>
PRIVATE_KEY="<Приватный ключ>"
CLIENT_EMAIL=<email сервисного аккаунта>
CLIENT_ID=<ID сервисного аккаунта>
AUTH_URI="https://accounts.google.com/o/oauth2/auth"
TOKEN_URI="https://oauth2.googleapis.com/token"
AUTH_PROVIDER_X509_CERT_URL="https://www.googleapis.com/oauth2/v1/certs"
CLIENT_X509_CERT_URL=<Cсылка на данные сервисного аккаунта>
EMAIL=<email пользователя>
```
#### Создание базы данных
``` bash
alembic upgrade head
```
#### Запуск
``` bash
uvicorn app.main:app
```
## Автор
[**Оганин Пётр**](https://github.com/NECROshizo) 
2023 г.