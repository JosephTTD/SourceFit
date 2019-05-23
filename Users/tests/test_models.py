from django.test import TestCase
from datetime import date, datetime


from Users.models import CustomUser, WeightMeasurementUnits, HeightMeasurementUnits


class EntryModelTest(TestCase):

    def test_maint_calories_representation(self):
        entry = CustomUser(weight=10, weightUnits=WeightMeasurementUnits.KG, height=10,
                           heightUnits=HeightMeasurementUnits.CM, dob=date(year=2000, month=5, day=10))
        self.assertEqual(34, entry.calculate_maintenance_calories())