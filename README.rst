Описание
--------
Рекомендационная система для УНТИ. Использует Python3.5+

Запуск
------

1. Создать и активировать virtualenv

  ::

   python -m virtualenv --python=/usr/bin/python3.5 env
   souce env/bin/activate


2. Установка пакетов

  ::

     pip install -r requirements.txt

3. Запуск миграций

  ::

    django-admin migrate

4. Установка периодического systemd/cron запуска management команды activity_recommendations_update

5. Создание файла edu_recsys/config.json на основе edu_recsys/config.json.example и его модификация
