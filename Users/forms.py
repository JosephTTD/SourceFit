import datetime
from django import forms
from .models import CustomUser
from .models import WeightMeasurementUnits
from .models import GenderEnum
from .models import HeightMeasurementUnits
from django.conf import settings
from django.forms import DateField
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter usrname or Email'}))
    password = forms.CharField(widget=PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'}))


class UserRegisterForm(UserCreationForm):

    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'example: healthlover101'}))
    dob = forms.DateField(required=True, widget=forms.SelectDateWidget(years=range(2019, 1920, -1), attrs={'class': 'date-form'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'example: you@mail.com'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'example: John'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'example: Smith'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'example: Your Password should be 6 or more characters'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'example: Confirm your password'}))
    gender = forms.ChoiceField(widget=forms.Select(attrs={'class': 'choice-form', 'placeholder': 'example: healthlover101'}), choices=[(sex.name, sex.value) for sex in GenderEnum])
    heightUnits = forms.ChoiceField(widget=forms.Select(attrs={'class': 'choice-form', 'placeholder': 'example: healthlover101'}), choices=[(unit.name, unit.value) for unit in HeightMeasurementUnits])
    weightUnits = forms.ChoiceField(widget=forms.Select(attrs={'class': 'choice-form', 'placeholder': 'example: healthlover101'}),choices=[(unit.name, unit.value) for unit in WeightMeasurementUnits])
    height = forms.IntegerField(  widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'example: Enter your height'}),)
    weight = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'example: Enter your weight'}), )

    def save(self, commit=True):
        user = super(UserRegisterForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.dob = self.cleaned_data["dob"]
        user.gender = self.cleaned_data["gender"]
        user.height = self.cleaned_data["height"]
        user.heightUnits = self.cleaned_data["heightUnits"]
        user.weightUnits = self.cleaned_data["weightUnits"]
        user.height = self.cleaned_data["height"]
        user.weight = self.cleaned_data["weight"]
        if commit:
            user.save()
        return user

    def clean(self):
        date = self.cleaned_data['dob']
        height = self.cleaned_data['height']
        weight = self.cleaned_data['weight']
        username = self.cleaned_data['username']
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(username=username).exists():
            raise forms.ValidationError("That username is already taken")
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError("That email is already taken")
        if date > datetime.date.today():
            raise forms.ValidationError("The date cannot be in the future!")
        if height <= 0:
            raise forms.ValidationError("Height must be positive!")
        if weight <= 0:
            raise forms.ValidationError("Weight must be positive!")
        return self.cleaned_data

    class Meta:
        model = get_user_model()
        fields = (
         'username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'dob', 'gender', 'heightUnits',
            'weightUnits', 'height', 'weight')
        labels = {
            'password1': _('Create a Password'),
            'password2' : _('Confirm your Password')
        }