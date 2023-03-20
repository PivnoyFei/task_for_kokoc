

[![Build Status](https://github.com/PivnoyFei/task_for_kokoc/actions/workflows/main.yml/badge.svg?branch=main)](https://github.com/PivnoyFei/task_for_kokoc/actions/workflows/main.yml)

<h1 align="center"><a target="_blank" href="">Тестовое задание для Kokoc</a></h1>


### Стек:
![Python](https://img.shields.io/badge/Python-171515?style=flat-square&logo=Python)![3.10](https://img.shields.io/badge/3.10-blue?style=flat-square&logo=3.10)
![Django](https://img.shields.io/badge/Django-171515?style=flat-square&logo=Django)![4.1.7](https://img.shields.io/badge/4.1.7-blue?style=flat-square&logo=4.1.7)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-171515?style=flat-square&logo=PostgreSQL)![13.0](https://img.shields.io/badge/13.0-blue?style=flat-square&logo=13.0)
![SQLite](https://img.shields.io/badge/SQLite-171515?style=flat-square&logo=SQLite)
![Nginx](https://img.shields.io/badge/Nginx-171515?style=flat-square&logo=Nginx)
![Pytest](https://img.shields.io/badge/Pytest-171515?style=flat-square&logo=Pytest)

### Задание
#### Создать сервис прохождения опросов пользователями на Django.
#### Обязательная часть:
1. Можно зарегистрироваться и логинится. Наверху показано под каким логином ты зашел.
2. Тесты и ответы на них создаются динамически через админку.
3. Список тестов выводится в виде содержания произвольного вида (столбец, таблица, как удобно) Фронт делается с помощью шаблонизатора Django, СУБД произвольная

### Опция 1.

1. За прохождение тестов начисляется какое-то количества валюты.
2. Валюту можно потратить на перекрашивание рамки логина или бэкграунда на странице профиля.
3. Показывать список пользователей и количество пройденных тестов на отдельной странице, там же показывать цветовую дифференциацию пользователей.

### Опция 2.
1. Сделать фронт на реакте, в виде SPA или отдельных модулей.



### Маршруты
| Название | Метод | Описание | Авторизация |
|----------|-------|----------|-------------|
| /                          | GET      | Список тестов и поиск по названию | нет
| test/<<int:pk>>/           | GET/POST | Страница теста                    | Да
| ...                        |          |                                   | 
| auth/signup/               | GET/POST | Зарегестрироваться                | Да
| auth/login/                | GET/POST | Авторизоваться                    | Да
| auth/logout/               | GET/POST | Выйти                             | Да
| users/                     | GET/POST | Список пользователей и количество пройденных тестов, и их цвета | Да
| profile/                   | GET/POST | Профиль пользователя с выбором купленных цветов                 | Да
| buy/                       | GET/POST | Список цветов доступных для покупки                             | Да


### Запуск проекта
Клонируем репозиторий и переходим в него:
```bash
gh clone https://github.com/PivnoyFei/task_for_kokoc.git
cd task_for_kokoc
```

### Перед запуском сервера, необходимо создать .env файл расположенный по пути infra/.env со своими данными.
### Ниже представлены параметры по умолчанию.
```bash
SECRET_KEY='key' # Секретный ключ джанго
DEBUG='True' # Режим разработчика
ALLOWED_HOSTS='localhost' # Адрес

DB_ENGINE='django.db.backends.postgresql'
DB_NAME='postgres' # имя БД
POSTGRES_USER='postgres' # логин для подключения к БД
POSTGRES_PASSWORD='postgres' # пароль для подключения к БД
DB_HOST='db' # название контейнера
DB_PORT='5432' # порт для подключения к БД
```

#### Чтобы сгенерировать безопасный случайный секретный ключ, используйте команду:
```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

### Для запуска в Docker:
#### Переходим в папку с файлом docker-compose.yaml:
```bash
cd infra
```

#### Запуск docker-compose:
```bash
docker-compose up -d --build
```

#### Примените миграции:
```bash
docker-compose exec backend python manage.py makemigrations
docker-compose exec backend python manage.py migrate --noinput
```

#### Загрузите подготовленные цвета в базу данных:
в папке data - ```colors.json```, ```tests.json```
```bash
docker-compose exec backend python manage.py load_items colors.json
```

#### Создайте суперпользователя Django:
```bash
docker-compose exec backend python manage.py createsuperuser
```

#### После успешной сборки, на сервере выполните команды (только после первого деплоя):
```bash
docker-compose exec backend python manage.py collectstatic --noinput
```

#### Теперь сервер доступен по адресу - http://localhost админка доступна по - http://localhost/admin/.

#### Останавливаем контейнеры:
```bash
docker-compose down -v
```

### Запуск на локальной машине:
#### Создаем и активируем виртуальное окружение в корневой папке task_for_kokoc, для выхода из папки введите команду ```cd ..```:
```bash
python3 -m venv venv
source venv/bin/activate
```
#### для Windows
```bash
python -m venv venv
source venv/Scripts/activate
```
#### Обновиляем pip и ставим зависимости из requirements.txt:
```bash
python -m pip install --upgrade pip
pip install -r backend/requirements.txt
```

#### Открываем в консоли папку backend:
```bash
cd backend
```

#### Обновиляем pip и ставим зависимости из requirements.txt:
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

#### Примените миграции:
```bash
python manage.py makemigrations
python manage.py migrate --noinput
```

#### Создайте суперпользователя Django:
```bash
python manage.py createsuperuser
```

#### Запускаем сервер:
```bash
python manage.py runserver
```

#### Теперь сервер доступен по адресу - http://localhost:8000 админка доступна по - http://localhost:8000/admin/.

#### Автор
[Смелов Илья](https://github.com/PivnoyFei)
