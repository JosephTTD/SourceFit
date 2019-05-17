from enum import Enum
from django.db import models

# Create your models here.


class GoalChoice(Enum):
    CUT: "Cut"
    MAINTAIN: "Maintain"
    BULK: "Bulk"


class Goal(models.Model):
    goalWeight = models.FloatField()
    goalChoice = models.CharField(max_length=3, choices=[(choice.name, choice.value) for choice in GoalChoice])