# Accounts
Проект для удобного хранения и управления своих аккаунтов сайтов.

## Install

Клонируйте данный репозиторий и перейдите в каталог Accounts.
```
git clone https://github.com/nikitakoltman/Accounts
cd Accounts
```
Создайте и активируйте виртуальное окружение python.
```
python3 -m venv env
source env/bin/activate
```
Установите зависимости.
```
pip install -r requirements.txt
```
Перейдите в каталог accounts и проведите миграции.
```
cd accounts
python3 manage.py migrate
```
Создайте пользователя.
```
python3 manage.py createsuperuser
```
Активируйте сервер и пользуйтесь.
```
python3 manage.py runserver
```
