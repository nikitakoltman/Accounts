# Accounts
Проект для удобного хранения и управления своими аккаунтами сайтов.

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
Перейдите в директорию configs, создайте копию файла config-example.py с названием config.py и заполните
в нем нужные параметры (переменные из config.py импортируются в settings.py).
```
cd accounts/configs
cp config-example.py config.py
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
