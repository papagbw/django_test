from enum import Enum

from django.db import models

class Color(Enum):
    red = 0
    orange = 1
    yellow = 2
    green = 3
    blue = 4
    purple = 5
    white = 6
    gray = 7
    black = 8


class Person(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)

    class Meta:
        unique_together = (("name", "surname"),)

    def __str__(self):
        return f"{self.name}-{self.surname}"


class Teacher(Person):
    pass


class Bookbag(models.Model):
    color = models.CharField(max_length=100,
                             choices=tuple((tag, tag.value) for tag in Color))


class Student(Person):
    # An example of a many-to-one relationship
    # between one `Teacher` and many `Student`s.
    hr_teacher = models.ForeignKey(Teacher,
                                   on_delete=models.SET_NULL,
                                   null=True)
    # An example of a one-to-one relationship between Student and Bookbag.
    bookbag = models.OneToOneField(Bookbag,
                                   on_delete=models.SET_NULL,
                                   null=True)


class Class(models.Model):
    topic = models.CharField(max_length=100)
    class_number = models.IntegerField()
    # A many-to-one relationship between one `Teacher` and many `Class`es.
    lecturer = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=False)
    # A many-to-many relationship between `Class`es and `Student`s.
    students = models.ManyToManyField(Student)

    class Meta:
        unique_together = (("class_number",), )
