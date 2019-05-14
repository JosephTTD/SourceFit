from enum import Enum
from datetime import date
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _


class HeightMeasurementUnits(Enum):
    CM = "Centimeter"
    IN = "Inch"
    FT = "Foot"
    M = "Meter"


class WeightMeasurementUnits(Enum):
    LB = "Pounds"
    KG = "Kilograms"
    ST = "Stone"


class GenderEnum(Enum):
    M = "Male"
    F = "Female"


# Custom User model class
class CustomUser(AbstractUser):

    email = models.EmailField(_('email address'), unique=True)
    dob = models.DateField(null=True)
    gender = models.CharField(max_length=2, choices=[(sex.name, sex.value) for sex in GenderEnum])
    heightUnits = models.CharField(max_length=4, choices=[(unit.name, unit.value) for unit in HeightMeasurementUnits])
    weightUnits = models.CharField(max_length=3, choices=[(unit.name, unit.value) for unit in WeightMeasurementUnits])
    height = models.FloatField(null=True)
    weight = models.FloatField(null=True)

    def calculate_age(self):
        today = date.today()
        return today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))

    def __str__(self):
        return self.username
