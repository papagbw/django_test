import os

import django
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_test.settings')
django.setup()

if __name__ == '__main__':
    with connection.cursor() as cursor:
        cursor.execute("DROP DATABASE school_db")
