#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

# python manage.py compile messages
mkdir -p static

python manage.py collectstatic --noinput

python manage.py makemigrations
python manage.py migrate

echo "
from django.contrib.auth import get_user_model;
from django.conf import settings
User = get_user_model()
kwargs = {
    settings.USERNAME_FIELD: '${DJANGO_SUPERUSER_EMAIL}'
}
if not User.objects.filter(**kwargs).exists():
    User.objects.create_superuser(
        '${DJANGO_SUPERUSER_EMAIL}',
        '${DJANGO_SUPERUSER_PASSWORD}'
    )

" | python manage.py shell || /bin/true

uvicorn core.asgi:application --host 0.0.0.0 --port 8000 --reload