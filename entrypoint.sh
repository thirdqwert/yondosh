# #!/bin/bash
# set -e  # Если любая команда завершится с ошибкой — скрипт остановится

# # Выполнить миграции
# python manage.py migrate

# # Собрать статику
# python manage.py collectstatic --noinput

# # Запустить сервис в зависимости от переменной SERVICE
# if [ "$SERVICE" = "django" ]; then
#     exec gunicorn yondosh_core.wsgi:application --bind 0.0.0.0:8000
# elif [ "$SERVICE" = "worker" ]; then
#     exec celery -A yondosh_core worker --loglevel=info
# elif [ "$SERVICE" = "beat" ]; then
#     exec celery -A yondosh_core beat --loglevel=info
# else
#     echo "Unknown SERVICE=$SERVICE"
#     exit 1
fi