from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name='Correo electrónico')
    student_id = models.CharField(max_length=20, unique=True, verbose_name='Matrícula')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'student_id']

    def __str__(self):
        return self.email

