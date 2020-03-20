import os

import django.db.utils

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_test.settings')
django.setup()

from django_test.school.models import Teacher


def find_teacher(*, search_str: str):
    return Teacher.objects.filter(name__startswith='T')


if __name__ == '__main__':

    try:
        new_teacher = Teacher(name='Tom', surname='Jones')
        new_teacher.save()
    except django.db.utils.IntegrityError as e:
        print('Teacher already exists!')

    print('loading teachers...')

    teachers = find_teacher(search_str='T')

    for t in teachers:
        print(f"Teacher starting with 'T': {t}")
