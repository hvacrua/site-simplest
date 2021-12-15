from django.forms import modelform_factory, TextInput, Select
from .models import Client, Translator


ClientForm = modelform_factory(Client, fields=['meeting', 'email', 'name', 'phone'],
                               widgets={
                                   'meeting': Select(attrs={
                                       'class': 'form-control', 'placeholder': 'Choose date of meeting (required)'
                                   }),
                                   'email': TextInput(attrs={
                                       'class': 'form-control','placeholder': 'Enter your email (required)'
                                   }),
                                   'name': TextInput(attrs={
                                       'class': 'form-control', 'placeholder': 'Enter your name (required)'
                                   }),
                                   'phone': TextInput(attrs={
                                       'class': 'form-control', 'placeholder': 'Enter your phone number (required)'
                                   })
                               })

TranslatorForm = modelform_factory(Translator, fields=['en', 'ua', 'ru'])
