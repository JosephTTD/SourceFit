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


class UserRecordManager(models.Manager):
    def for_user(self, user):
        return self.get_queryset().filter(creator=user)


class UserRecord(models.Model):
    objects = UserRecordManager()


class Diet(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class DietData(models.Model):
    DietLog = models.ForeignKey('Diet', related_name='Log_of_data', on_delete=models.DO_NOTHING)
    FoodOrDrinkName = models.CharField(null=True,max_length=100)
    CalorificCount = models.IntegerField(null=True)
    TypeOfMeal = models.CharField(null=True,max_length=3, choices=[(type.name, type.value) for type in MealType])
    dateAdded = models.DateTimeField(null=True, default=datetime.now, blank=True)


class Activity(models.Model):
    ExerciseLog = models.ForeignKey('ExerciseTemplate', related_name='Exercise_Log_Of_Activities', on_delete=models.DO_NOTHING)
    ActivityDistance = models.IntegerField(null=True)
    ActivityDuration = models.TimeField(null=True)
    ActivityName = models.CharField(null=True,max_length=100)
    TypeOfActivity = models.CharField(null=True,max_length=9, choices=[(type.name, type.value) for type in ActivityType])
    Completion = models.BooleanField()


class ExerciseTemplate(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)


class Goal(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    goalWeight = models.FloatField(null=True)
    weightUnits = models.CharField(null=True, max_length=3, choices=[(unit.name, unit.value) for unit in WeightMeasurementUnits])
    goalDate = models.DateField(null=True)
    typeOfGoal = models.CharField(null=True, max_length=3, choices=[(unit.name, unit.value) for unit in GoalType])
    goalCompletion = models.BooleanField()
    goalExceeded = models.BooleanField()

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
        elif self.typeOfGoal == GoalType.MAINTAIN and ((goalWeight-float(2)) <= userWeight <= (goalWeight-float(2))):
            self.goalCompletion = True
            return True
        elif self.typeOfGoal == GoalType.GAIN and userWeight > goalWeight:
            self.goalCompletion = True
            return True
        return False

    def return_days_to_goal(self):
        if self.goalCompletion or self.goalExceeded:
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
    gender = models.CharField(max_length=2, choices=[(sex.name, sex.value) for sex in GenderEnum])
    heightUnits = models.CharField(max_length=4, choices=[(unit.name, unit.value) for unit in HeightMeasurementUnits])
    weightUnits = models.CharField(max_length=3, choices=[(unit.name, unit.value) for unit in WeightMeasurementUnits])
    exerciseIntensity = models.CharField(max_length=4, choices=[(intensity.name, intensity.value) for intensity in ExerciseIntensity])
    height = models.FloatField(null=True)
    weight = models.FloatField(null=True)

    def calculate_age(self):
        today = date.today()
        return today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))

    def calculate_bmi(self):
        height = Conversions.from_height_units_to_m(self.heightUnits, self.height)
        weight = Conversions.from_weight_units_to_kg(self.weightUnits, self.weight)
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
        return (float(10) * self.weight) + ((float(6.25) * self.height) - float(5)) * self.calculate_age()

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
