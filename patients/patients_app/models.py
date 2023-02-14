from django.db import models


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
