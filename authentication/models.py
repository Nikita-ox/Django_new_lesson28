from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):  # Чистая таблица
    MALE = 'm'  # Ключ
    FEMALE = 'f'  # Ключ
    SEX = [(MALE, 'Male'), (FEMALE, 'Female')]  # Список, который будет поставляться как значение
    '''Django формы'''

    HR ='hr'
    EMPLOYEE = 'employee'
    UNKNOWN = 'unknown'

    ROLE = [(HR, HR), (EMPLOYEE, EMPLOYEE), (UNKNOWN, UNKNOWN)]


    sex = models.CharField(max_length=1, choices=SEX, default=MALE)  # поставляться как значение
    role = models.CharField(max_length=8, choices=ROLE, default=UNKNOWN)
