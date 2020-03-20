from django.db import models


class Person(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)

    class Meta:
        unique_together = (("name", "surname"),)

    def __str__(self):
        return f"{self.name}-{self.surname}"


class Teacher(Person):
    pass


class Student(Person):
    pass
