from django.forms import ModelForm
from django import forms
from .models import EmailData

class EmailForm(forms.ModelForm):
    class Meta:
        model = EmailData
        fields = ('email',)

