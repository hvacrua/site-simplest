from django.db import models
from django.core.validators import RegexValidator


class Translator(models.Model):
    unique_name = models.CharField(max_length=128, unique=True)
    en = models.TextField()
    ua = models.TextField()
    ru = models.TextField()

    def __str__(self):
        return f'{self.en}, {self.ua}, {self.ru}'



class Client(models.Model):
    DATE_CHOICES = [
		('08/12', "Meeting on 08/12/2021"),
		('15/12', "Meeting on 15/12/2021"),
		('22/12', "Meeting on 22/12/2021")
	]

    phone_regex = RegexValidator(regex=r'^\+?1?\d{10,13}$',
								 message="Phone number must be entered in the format: '+380XXddddddd'. Up to 13 digits allowed.")

    meeting = models.CharField(max_length=30, null=False, choices=DATE_CHOICES, name='meeting')
    email = models.EmailField(unique=True, name='email')
    name = models.CharField(max_length=30, null=False, name='name')
    phone = models.CharField(validators=[phone_regex],  # validators should be a list
							 max_length=13, null=False,
							 unique=True, name='phone')

    def __str__(self):
        return f'{self.meeting}, {self.email}, {self.name}, {self.phone}'
