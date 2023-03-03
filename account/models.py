from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class AccountManager(BaseUserManager):
    def create_user(self, firstName, lastName, email, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            firstName=firstName,
            email=self.normalize_email(email),
            lastName=lastName
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    # def create_superuser(self, email, password=None):
    #     """
    #     Creates and saves a superuser with the given email, date of
    #     birth and password.
    #     """
    #     user = self.create_user(
    #         email,
    #         password=password
    #     )
    #     user.save(using=self._db)
    #     return user

class Account(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    firstName = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
  
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = AccountManager()

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True