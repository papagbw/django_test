import os

import django.db.utils

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_test.settings')
django.setup()

from django_test.school.models import Teacher, Student


def find_teacher(*, search_str: str):
    return Teacher.objects.filter(name__startswith='T')


def create_teacher(*, name: str, surname: str):
    try:
        new_teacher = Teacher(name=name, surname=surname)
        new_teacher.save()
    except django.db.utils.IntegrityError:
        print('Teacher already exists!')


def create_student(*, name: str, surname: str):
    try:
        new_student = Student(name=name, surname=surname)
        new_student.save()
    except django.db.utils.IntegrityError:
        print('Student already exists!')


if __name__ == '__main__':

    create_teacher(name='Tom', surname='Jones')
    create_student(name='Betsy', surname='Ross')
    create_student(name='Bob', surname='Ross')
    create_student(name='Ross', surname='Fromfriends')

    print('loading teachers...')

    teachers = find_teacher(search_str='T')

    for t in teachers:
        print(f"Teacher starting with 'T': {t}")

    homeroom_teacher = Teacher.objects.get(pk=1)

    for s in Student.objects.all():
        homeroom_teacher.student_set.add(s)
    homeroom_teacher.save()

    for s in homeroom_teacher.student_set.all():
        print(s)
