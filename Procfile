release: cd vansgram_backend && python manage.py migrate
web: daphne vansgram_backend.vansgram_backend.asgi:application --port $PORT --bind 0.0.0.0 -v2
celery: cd vansgram_backend && celery -A vansgram_backend.vansgram_backend.celery worker -l info
celerybeat: cd vansgram_backend && celery -A vansgram_backend.vansgram_backend beat -l INFO
celeryworker2: cd vansgram_backend && celery -A vansgram_backend.vansgram_backend.celery worker & celery -A vansgram_backend.vansgram_backend beat -l INFO & wait -n