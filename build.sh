#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no manage.py migrate` հրամանը, հավանաբար, նայում է `django_migrations` աղյուսակին (որը `--fake`-ը լրացրել էր) և մտածում է. «Ամեն ինչ արդեն միգրացված է, անելիք չունեմ»։ Արդյունքում, այն չի ստեղծում բացակայող `django_session-input

# Սա կփորձի կիրառել բոլոր միգրացիաները
python manage.py migrate

# Սա կոնկրետ կստիպի ստեղծել sessions աղյուսակը, եթե այն բացակայում է
python manage.py migrate sessions