import logging
import os

import django.db.utils
from django.db.models.query import QuerySet

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_test.settings')
django.setup()

from django_test.school.models import Teacher, Student, Class, Bookbag, Color

_log = logging.getLogger(__name__)


def find_teacher(*, search_str: str) -> QuerySet:
    return Teacher.objects.filter(name__startswith=search_str)


def create_or_get_teacher(*, name: str, surname: str) -> Teacher:
    try:
        teacher = Teacher(name=name, surname=surname)
        teacher.save()
    except django.db.utils.IntegrityError:
        _log.debug('Teacher already exists!')
        teacher = Teacher.objects.filter(name=name, surname=surname).first()

    return teacher


def create_or_get_class(*,
                        topic: str,
                        class_number: int,
                        lecturer: Teacher) -> Class:
    try:
        class_ = Class(topic=topic,
                       class_number=class_number,
                       lecturer=lecturer)
        class_.save()
    except django.db.utils.IntegrityError:
        _log.debug('Class already exists!')
        class_ = Class.objects.filter(class_number=class_number).first()

    return class_


def create_student(*, name: str, surname: str):
    try:
        new_student = Student(name=name, surname=surname)
        new_student.save()
    except django.db.utils.IntegrityError:
        _log.debug('Student already exists!')


if __name__ == '__main__':
    homeroom_teacher = create_or_get_teacher(name='Tom', surname='Jones')

    for teacher_name in ('Marcel Wallace', 'The Bride', 'Princess Leia'):
        name, surname = teacher_name.split(' ')
        create_or_get_teacher(name=name, surname=surname)

    create_student(name='Betsy', surname='Ross')
    create_student(name='Bob', surname='Ross')
    create_student(name='Ross', surname='Fromfriends')

    # Give students bookbags.
    for name, color in (('Betsy', Color.blue),
                        ('Bob', Color.blue),
                        ('Ross', Color.black)):
        s = Student.objects.filter(name=name).first()
        b = Bookbag(color=color)
        s.bookbag = b
        b.save()
        s.save()

    # Create semester classes.
    classes = []
    classes.append(create_or_get_class(topic='Reading',
                                       class_number=101,
                                       lecturer=create_or_get_teacher(name='Marcel', surname='Wallace')))
    classes.append(create_or_get_class(topic='Writing',
                                       class_number=102,
                                       lecturer=create_or_get_teacher(name='The', surname='Bride')))
    classes.append(create_or_get_class(topic='Arithmetic',
                                       class_number=103,
                                       lecturer=create_or_get_teacher(name='Princess', surname='Leia')))

    print('loading teachers...')

    # Search for teachers whose names start with T
    for t in find_teacher(search_str='T'):
        print(f"Teacher starting with 'T': {t}")

    # All students have Tom Jones as their homeroom teacher.
    for s in Student.objects.all():
        homeroom_teacher.student_set.add(s)
    homeroom_teacher.save()

    # Betsy Ross is removed from Tom Jones's homeroom class.
    s = Student.objects.filter(name='Betsy', surname='Ross').first()
    homeroom_teacher.student_set.remove(s)
    homeroom_teacher.save()

    # Print the names of all students in Tom Jones's homeroom class.
    print("**********************************************")
    print("The students in Tom Jones's homeroom class are")
    for s in homeroom_teacher.student_set.all():
        print(s)

    # All students take all classes:
    for c in classes:
        for s in Student.objects.all():
            c.students.add(s)

    # Show students in the Reading class
    print("**************************************")
    print("The students in the Reading class are:")
    for s in Class.objects.filter(class_number=101).first().students.all():
        print(s)

    # If you wanted to delete a Class
    # c_reading = Class.objects.filter(topic='Reading').delete()

    print("***************")
    print("The classes are")
    for c in Class.objects.all():
        print(c.topic)

    # Find all students with blue bookbags - there is a join being implemented
    # under the hood.
    print("*******************************")
    print("The students with blue bags are")
    for s in Student.objects.filter(bookbag__color__contains="blue"):
        print(s)
        s.save()
