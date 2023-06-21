from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField


class Client(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    age = models.PositiveSmallIntegerField(null=True, blank=True)
    phone = PhoneNumberField(null=True, blank=True)
    full_address = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        ordering = ('user',)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'
