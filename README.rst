Описание
--------
Рекомендационная система для УНТИ. Использует Python3.5+

Запуск
------

1. Создать и активировать virtualenv

  ::

   python -m virtualenv --python=/usr/bin/python3.5 env
   souce env/bin/activate


2. Установка пакетов и apt-requirements

  ::

    pip install -r requirements.txt

3. Настройка базы и редактирование config.json на основе config.json.example. База должна быть с кодировкой UTF8

  ::

    CREATE DATABASE IF NOT EXISTS %s CHAR SET 'UTF8'



4. Запуск миграций

  ::

    python manage.py migrate

5. Установка периодического systemd/cron запуска management команд update_activity_recommendations, update_networking_recommendations, load_activities

6. Подгрузка дефолтных данных в базу

  ::

    python manage.py loaddata context
