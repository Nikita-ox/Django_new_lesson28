
from django.db import models

from authentication.models import User


class Skill(models.Model):
    name = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)


    class Meta:
        verbose_name = "Навык"
        verbose_name_plural = "Навыки"


    def __str__(self):
        return self.name




class Vacancy(models.Model):
    STATUS = [
        ("draft", "Человек"),
        ("open", "Открыто"),
        ("closed", "Закрыто"),
    ]


    slug = models.SlugField(max_length=50)
    text = models.CharField(max_length=2000)
    status = models.CharField(max_length=6, choices=STATUS, default="draft")
    created = models.DateField(auto_now_add=True)
    users = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    skill = models.ManyToManyField(Skill)

    likes = models.IntegerField(default=0)


    def __str__(self):
        return str(self.text)

    class Meta:
        verbose_name = "Вакансия"
        verbose_name_plural = "Вакансии"
        # ordering = ["test"]


    @property
    def username(self):
        return self.users.username if self.users else None





