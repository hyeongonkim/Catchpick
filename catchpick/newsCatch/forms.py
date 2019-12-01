from django.forms import ModelForm
from django import forms
from .models import EmailData

class EmailForm(forms.ModelForm):
    email = forms.CharField(
        widget=forms.EmailInput(
            attrs={'class': 'input100', 'name': 'email'}
        )
    )

    class Meta:
        model = EmailData
        fields = ('email',)

