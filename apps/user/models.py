from django.db import models

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class Type(models.IntegerChoices):
        ADMIN = (1, 'Admin')
        SECRETARY = (2, 'Secretary')
    email = models.EmailField(unique=True)
    user_type = models.PositiveSmallIntegerField(choices=Type.choices,
                                                 default=Type.ADMIN)
    phone = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        db_table = 'users'

    def __str__(self):
        return self.username
