from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, email: str, password: str | None = None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        if not extra_fields.get('display_name'):
            raise ValueError('Display name is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email: str, password: str | None = None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('Електронна пошта', unique=True)
    display_name = models.CharField("Ім'я", max_length=80)
    is_staff = models.BooleanField('Адміністратор', default=False)
    is_active = models.BooleanField('Активний', default=True)
    date_joined = models.DateTimeField('Дата реєстрації', default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS: list[str] = ['display_name']

    class Meta:
        ordering = ['email']
        verbose_name = 'Користувач'
        verbose_name_plural = 'Користувачі'

    def __str__(self) -> str:
        return self.display_name or self.email

# Create your models here.
