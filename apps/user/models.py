from django.db import models

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class type(models.IntegerChoices):
        ADMIN = (1, 'Admin')
        SECRETARY = (1, 'Secretary')

    email = models.EmailField(unique=True)
    user_type = models.PositiveSmallIntegerField(choices=type.choices)
    phone = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        db_table = 'users'

    def __str__(self):
        return self.username
