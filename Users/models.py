from enum import Enum
from datetime import date, datetime
from django.db import models
from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.timezone import localtime, now
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _


class ExerciseIntensity(Enum):
    SEDENTARY = "Sedentary"
    LIGHT = "Light"
    MODERATE = "Moderate"
    INTENSE = "Intense"


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


class GoalChoice(Enum):
    CUT = "Cut"
    MAINTAIN = "Maintain"
    BULK = "Bulk"


class ActivityType(Enum):
    RUNNING = "Running"
    SWIMMING = "Swimming"
    JOGGING = "Jogging"
    WALKING = "Walking"
    HIIT = "High Intensity Interval Training"
    FREE_WEIGHT = "Free Weights"
    WEIGHT_MACHINES = "Weight Machines"
    YOGA = "Yoga"
    OTHER = "Other"


class HealthinessLevel(Enum):
    UNDERWEIGHT = "underweight"
    HEALTHY = "healthy"
    OVERWEIGHT = "overweight"
    OBESE = "obese"


class MealType(Enum):
    BREAKFAST = "Breakfast"
    LUNCH = "Lunch"
    DINNER = "Dinner"


class GoalType(Enum):
    LOSE = "Lose Weight"
    MAINTAIN = "Maintain Weight"
    GAIN = "Gain Weight"


class DietData(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_diet', null=True, blank=True)
    foodOrDrinkName = models.CharField(null=True, max_length=100)
    calorificCount = models.IntegerField(null=True)
    typeOfMeal = models.CharField(default=MealType.LUNCH, max_length=3, choices=[(type.name, type.value) for type in MealType])
    dateAdded = models.DateTimeField(default=datetime.now, blank=True)


class Activity(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_activity', null=True, blank=True)
    activityDistance = models.IntegerField(null=True)
    activityDuration = models.IntegerField(null=True)
    activityName = models.CharField(null=True, max_length=100)
    typeOfActivity = models.CharField(default=ActivityType.RUNNING, max_length=9,
                                      choices=[(type.name, type.value) for type in ActivityType])
    completion = models.BooleanField(default=False)


class Goal(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    goalWeight = models.FloatField(null=True)
    weightUnits = models.CharField(default=WeightMeasurementUnits.KG, max_length=50,
                                   choices=[(unit.name, unit.value) for unit in WeightMeasurementUnits])
    goalDate = models.DateField(null=True)
    typeOfGoal = models.CharField(default=GoalType.MAINTAIN, max_length=50, choices=[(unit.name, unit.value) for unit in GoalType])
    goalCompletion = models.BooleanField(default=False)
    goalExceeded = models.BooleanField(default=False)

    def check_goal_is_expired(self):
        if date.today() >= self.goalDate:
            self.goalExceeded = True
            return True
        return False

    def check_goal_is_complete(self, user_weight_units, user_weight):
        goalWeight = Conversions.from_weight_units_to_kg(self.weightUnits, self.goalWeight)
        userWeight = Conversions.from_weight_units_to_kg(user_weight_units, user_weight)
        if self.typeOfGoal == GoalType.LOSE and userWeight < goalWeight:
            self.goalCompletion = True
            return True
        elif self.typeOfGoal == GoalType.MAINTAIN and (
                (goalWeight - float(2)) <= userWeight <= (goalWeight - float(2))):
            self.goalCompletion = True
            return True
        elif self.typeOfGoal == GoalType.GAIN and userWeight > goalWeight:
            self.goalCompletion = True
            return True
        return False

    def return_days_to_goal_deadline(self):
        if self.goalCompletion or self.goalExceeded or self.goalDate is None:
            return 0
        return (self.goalDate - date.today()).days


class Conversions:

    @staticmethod
    def weight_pounds_to_kg(weight):
        return weight / 2.20462262

    @staticmethod
    def weight_stone_to_kg(weight):
        return weight * 6.35029

    @staticmethod
    def height_centimeters_to_meters(height):
        return height / float(100)

    @staticmethod
    def height_feet_to_meters(height):
        return height * 0.3048

    @staticmethod
    def height_inches_to_meters(height):
        return height * 0.0254

    @staticmethod
    def from_weight_units_to_kg(weight_units, weight):
        temp_weight = weight
        if weight_units == WeightMeasurementUnits.LB:
            temp_weight = Conversions.weight_pounds_to_kg(weight)
        elif weight_units == WeightMeasurementUnits.ST:
            temp_weight = Conversions.weight_stone_to_kg(weight)
        return temp_weight

    @staticmethod
    def from_height_units_to_m(height_units, height):
        temp_height = height
        if height_units == HeightMeasurementUnits.CM:
            temp_height = Conversions.height_centimeters_to_meters(height)
        elif height_units == HeightMeasurementUnits.FT:
            temp_height = Conversions.height_feet_to_meters(height)
        elif height_units == HeightMeasurementUnits.IN:
            temp_height = Conversions.height_inches_to_meters(height)
        return temp_height


# Custom User model class
class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    dob = models.DateField(null=True)
    gender = models.CharField(default=GenderEnum.M, max_length=2, choices=[(sex.name, sex.value) for sex in GenderEnum])
    heightUnits = models.CharField(default=HeightMeasurementUnits.M, max_length=4, choices=[(unit.name, unit.value) for unit in HeightMeasurementUnits])
    weightUnits = models.CharField(default=WeightMeasurementUnits.KG, max_length=3, choices=[(unit.name, unit.value) for unit in WeightMeasurementUnits])
    exerciseIntensity = models.CharField(default=ExerciseIntensity.MODERATE,max_length=50,
                                         choices=[(intensity.name, intensity.value) for intensity in ExerciseIntensity])
    height = models.FloatField(null=True)
    weight = models.FloatField(null=True)

    def calculate_age(self):
        today = date.today()
        return today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))

    def calculate_bmi(self, h_units, h, w_units, w):
        height = Conversions.from_height_units_to_m(h_units, h)
        weight = Conversions.from_weight_units_to_kg(w_units, w)
        return round(weight / (height * height), 2)

    def calculate_maintenance_calories(self):
        bmr = self.calculate_bmr()

        if self.gender == GenderEnum.F:
            bmr -= float(161)
        else:
            bmr += float(5)
        if self.exerciseIntensity == ExerciseIntensity.SEDENTARY:
            bmr *= float(1.2)
        elif self.exerciseIntensity == ExerciseIntensity.LIGHT:
            bmr *= float(1.375)
        elif self.exerciseIntensity == ExerciseIntensity.MODERATE:
            bmr *= float(1.55)
        else:
            bmr *= float(1.725)
        return round(bmr, 2)

    def calculate_bmr(self):
        height = Conversions.from_height_units_to_m(self.heightUnits, self.height) * float(100)
        weight = Conversions.from_weight_units_to_kg(self.weightUnits, self.weight)
        return (float(10) * weight) + ((float(6.25) * height) - float(5)) * float(self.calculate_age())

    def calculate_healthiness(self):
        bmi = self.calculate_bmi()
        if bmi < float(18.5):
            return HealthinessLevel.UNDERWEIGHT.value
        elif bmi < float(25):
            return HealthinessLevel.HEALTHY.value
        elif bmi < float(30):
            return HealthinessLevel.OVERWEIGHT.value
        else:
            return HealthinessLevel.OBESE.value

    def __str__(self):
        return self.username
