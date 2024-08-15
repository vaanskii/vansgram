release: python manage.py migrate
web: daphne vansgram_backend.asgi:application --port $PORT --bind 0.0.0.0 -v2
celery: celery -A vansgram_backend.celery worker -l info
celerybeat: celery -A vansgram_backend beat -l INFO 
celeryworker2: celery -A vansgram_backend.celery worker & celery -A vansgram_backend beat -l INFO & wait -n