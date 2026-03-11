from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    SEX_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    height_cm = models.FloatField(blank=True, null=True)
    weight_kg = models.FloatField(blank=True, null=True)
    age = models.PositiveIntegerField(blank=True, null=True)
    sex = models.CharField(max_length=10, choices=SEX_CHOICES, blank=True)

    bmi_value = models.FloatField(blank=True, null=True)
    bmi_category = models.CharField(max_length=20, blank=True)

    def calculate_bmi(self):
        if not self.height_cm or not self.weight_kg:
            return None

        height_m = self.height_cm / 100
        if height_m <= 0:
            return None

        return round(self.weight_kg / (height_m ** 2), 1)

    def get_bmi_category(self):
        bmi = self.calculate_bmi()
        if bmi is None:
            return ''

        if bmi < 18.5:
            return 'Underweight'
        elif bmi < 25:
            return 'Normal'
        elif bmi < 30:
            return 'Overweight'
        return 'Obese'

    def save(self, *args, **kwargs):
        if self.height_cm is not None:
            self.height_cm = round(self.height_cm, 1)
        if self.weight_kg is not None:
            self.weight_kg = round(self.weight_kg, 1)

        self.bmi_value = self.calculate_bmi()
        self.bmi_category = self.get_bmi_category()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username}'s profile"


class DailyGoal(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    target_calories = models.PositiveIntegerField(default=2000)
    target_protein = models.FloatField(default=100)
    target_carbs = models.FloatField(default=250)
    target_fat = models.FloatField(default=70)

    def __str__(self):
        return f"{self.user.username}'s daily goals"

    def save(self, *args, **kwargs):
        self.target_protein = round(self.target_protein, 1)
        self.target_carbs = round(self.target_carbs, 1)
        self.target_fat = round(self.target_fat, 1)
        super().save(*args, **kwargs)