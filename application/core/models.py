from django.db import models
from django.contrib.auth.models import (AbstractBaseUser,
                                        BaseUserManager, PermissionsMixin)


class CustomUserManager(BaseUserManager):

    def create_user(self, email, password, **kwargs):
        if not email:
            raise ValueError('No Email Provided')
        user = self.model(email=self.normalize_email(email), **kwargs)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, *args, **kwargs):
        user = self.create_user(*args, **kwargs)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom User model handle signup using email
    """

    GENDER_CHOICES = (
        ('m', 'Male'), ('f', 'Female'), ('o', 'Other')
    )

    email = models.EmailField(
        max_length=255,
        unique=True, null=False, blank=False)
    name = models.CharField(max_length=255)
    age = models.PositiveSmallIntegerField(default=1)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=3)
    mobile = models.CharField(max_length=255, unique=True)
    land_line = models.CharField(max_length=255, unique=True)
    country = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    career = models.CharField(max_length=255)

    objects = CustomUserManager()

    # Customize the username
    USERNAME_FIELD = 'email'
