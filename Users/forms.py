from django import forms
from .models import CustomUser
from django.conf import settings
from django.forms import DateField
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):

    dob = DateField(input_formats=settings.DATE_INPUT_FORMATS)
    email = forms.EmailField()

    class Meta:
        model = CustomUser
        fields = (
            'username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'dob', 'gender', 'heightUnits',
            'weightUnits', 'height', 'weight',)
