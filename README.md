# Hillel_support


## Application setup
```bash
pip install pipenv

pipenv shell
pipenv sync --dev

gunicorn src.main:application --reload
```

## Celery workers start

```bash
pipenv shell
celery worker -A config ...
```