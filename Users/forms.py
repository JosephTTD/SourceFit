import datetime
from django import forms
from .models import CustomUser
from django.conf import settings
from django.forms import DateField
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):

    dob = forms.DateField(required=True, widget=forms.SelectDateWidget(years=range(2019, 1920, -1)))
    email = forms.EmailField()

    def save(self, commit=True):
        user = super(UserRegisterForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.dob = self.cleaned_data["dob"]
        user.gender = self.cleaned_data["gender"]
        user.heightUnits = self.cleaned_data["heightUnits"]
        user.weightUnits = self.cleaned_data["weightUnits"]
        user.height = self.cleaned_data["height"]
        user.weight = self.cleaned_data["weight"]
        if commit:
            user.save()
        return user

    def clean_date(self):
        date = self.cleaned_data['dob']
        if date > datetime.date.today():
            raise forms.ValidationError("The date cannot be in the future!")
        return date

    class Meta:
        model = CustomUser
        fields = (
            'username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'dob', 'gender', 'heightUnits',
            'weightUnits', 'height', 'weight',)