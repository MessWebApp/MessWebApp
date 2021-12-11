from django import forms
from django.db import models
from django.forms import fields

from .models import ContactMe,MessDetails


class ContactForm(forms.Form):
    class Meta:
        models = ContactMe
        fields = ('name','email','number','message')

