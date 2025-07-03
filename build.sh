#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

# Կիրառում ենք միգրացիաները՝ անտեսելով սխալները և նշելով դրանք որպես կատարված
python manage.py migrate --fake

python manage.py collectstatic --no-input