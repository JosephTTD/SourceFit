import datetime
from django import forms
from .models import Goal, GoalType, MealType, DietData, ActivityType, Activity
from .models import WeightMeasurementUnits
from .models import GenderEnum
from .models import HeightMeasurementUnits
from .models import ExerciseIntensity
from django.conf import settings
from django.forms import DateField
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput


class GoalCreationForm(forms.Form):
    goalWeight = forms.FloatField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'example: Enter your goal weight'}), )
    weightUnits = forms.ChoiceField(widget=forms.Select(attrs={'class': 'choice-form', 'placeholder': ''}),choices=[(unit.name, unit.value) for unit in WeightMeasurementUnits])
    goalDate = forms.DateField(widget=forms.SelectDateWidget(years=range(2019, 2070),attrs={'class': 'date-form'}))
    typeOfGoal = forms.ChoiceField(widget=forms.Select(attrs={'class': 'choice-form', 'placeholder': ''}), choices=[(unit.name, unit.value) for unit in GoalType])

    def clean(self):
        date = self.cleaned_data['goalDate']
        weight = self.cleaned_data['goalWeight']

        if date < datetime.date.today():
            raise forms.ValidationError("Goal date can't be in the past")
        if not weight:
            raise forms.ValidationError("You must enter a goal weight")
        return self.cleaned_data

    class Meta:
        model = Goal
        fields = ('goalWeight', 'weightUnits', 'goalDate', 'typeOfGoal')


class ActivityCreationForm(forms.Form):
    activityDistance = forms.IntegerField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'example: Enter your goal distance in m'}), )
    activityDuration = forms.TimeField()
    activityName = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter activity name'}), )
    typeOfActivity = forms.ChoiceField(widget=forms.Select(attrs={'class': 'choice-form', 'placeholder': ''}),
                                       choices=[(type.name, type.value) for type in ActivityType])

    def clean(self):
        name = self.cleaned_data['activityName']
        distance = self.cleaned_data['activityDistance']
        duration = self.cleaned_data['activityDuration']

        if not (distance or duration):
            raise forms.ValidationError("You must at least one of distance or duration")
        if not name:
            raise forms.ValidationError("You must enter an activity name")
        return self.cleaned_data

    class Meta:
        model = Activity
        fields = ('activityName','activityDuration', 'activityDistance', 'typeOfActivity',)


class DietCreationForm(forms.Form):
    calorificCount = forms.FloatField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'example: Enter the calories'}), )
    typeOfMeal = forms.ChoiceField(widget=forms.Select(attrs={'class': 'choice-form', 'placeholder': ''}),
                                   choices=[(type.name, type.value) for type in MealType])
    foodOrDrinkName = forms.CharField(widget=forms.TimeInput(attrs={'class': 'choice-form', 'placeholder': ''}), )

    def clean(self):
        name = self.cleaned_data['foodOrDrinkName']
        calories = self.cleaned_data['calorificCount']

        if not calories:
            raise forms.ValidationError("You must enter some Calories")
        if not name:
            raise forms.ValidationError("You must enter a name for your food/drink")
        return self.cleaned_data

    class Meta:
        model = DietData
        fields = ('foodOrDrinkName', 'calorificCount', 'typeOfMeal',)


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter usrname or Email'}))
    password = forms.CharField(widget=PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'}))


class UserRegisterForm(UserCreationForm):

    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'example: healthlover101'}))
    dob = forms.DateField(label="Date of Birth", required=True, widget=forms.SelectDateWidget(years=range(2019, 1920, -1), attrs={'class': 'date-form'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'example: you@mail.com'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'example: John'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'example: Smith'}))
    password1 = forms.CharField(label = "Create Password", widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Your Password should be 6 or more characters'}))
    password2 = forms.CharField(label = "Confirm your mom", widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'example: Confirm your password'}))
    gender = forms.ChoiceField(widget=forms.Select(attrs={'class': 'choice-form', 'placeholder': ''}), choices=[(sex.name, sex.value) for sex in GenderEnum])
    heightUnits = forms.ChoiceField(widget=forms.Select(attrs={'class': 'choice-form', 'placeholder': ''}), choices=[(unit.name, unit.value) for unit in HeightMeasurementUnits])
    weightUnits = forms.ChoiceField(widget=forms.Select(attrs={'class': 'choice-form', 'placeholder': ''}),choices=[(unit.name, unit.value) for unit in WeightMeasurementUnits])
    height = forms.IntegerField(  widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'example: Enter your height'}),)
    weight = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'example: Enter your weight'}), )
    exerciseIntensity = forms.ChoiceField(widget=forms.Select(attrs={'class': 'choice-form', 'placeholder': ''}), choices=[(intensity.name, intensity.value) for intensity in ExerciseIntensity])

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
        user.exerciseIntensity = self.cleaned_data["exerciseIntensity"]
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
        if not (weight or height or date):
            raise forms.ValidationError("You are missing some fields")
        return self.cleaned_data

    class Meta:
        model = get_user_model()
        fields = (
         'username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'dob', 'gender', 'height', 'heightUnits',
            'weight', 'weightUnits', 'exerciseIntensity')