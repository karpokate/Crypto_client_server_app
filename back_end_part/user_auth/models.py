from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from rest_framework.authentication import TokenAuthentication

# Create your models here.

class UserManager(BaseUserManager):

    def create_user(self, email, name, home_address, phone_number, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        if not name:
            raise ValueError('Users must have an name')
        if not home_address:
            raise ValueError('Users must have an home_address')
        if not phone_number:
            raise ValueError('Users must have an phone_number')


        user = self.model(
            email=self.normalize_email(email),
            name=name,
            home_address=home_address,
            phone_number=phone_number,
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, home_address, phone_number, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email=email,
            name=name,
            home_address=home_address,
            phone_number=phone_number,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):

    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    name = models.CharField(
        verbose_name='name',
        max_length=64,
        default='user_name'
    )
    phone_number = models.CharField(
        verbose_name='phone_number',
        max_length=12,
        default='380000000000',
    )
    home_address = models.CharField(
        verbose_name='home_address',
        max_length=100,
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'phone_number', 'home_address']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin