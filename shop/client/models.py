from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField


class Client(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    age = models.PositiveSmallIntegerField()
    phone = PhoneNumberField()
    full_address = models.CharField(max_length=100)

    class Meta:
        ordering = ('user',)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'