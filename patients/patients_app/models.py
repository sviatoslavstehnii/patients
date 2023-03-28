from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class Patient(models.Model):
    """Model representing a patient."""
    SEXES = [('m', 'male'), ('f', 'female')]
    name = models.CharField(max_length=200)
    age = models.IntegerField()
    sex = models.CharField(choices=SEXES, max_length=1)
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    doctor = models.CharField(max_length=200)
    date = models.DateField()
    medical_history = models.TextField()

    def __str__(self) -> str:
        return str(self.name)

    class META:
        """Meta class for Patient model."""
        ordering = ['name']

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email address must be provided')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser):
    
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_anonymous = False
    is_authenticated = True
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()
    
