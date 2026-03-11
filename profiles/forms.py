from django import forms
from .models import UserProfile, DailyGoal


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['height_cm', 'weight_kg', 'age', 'sex']


class DailyGoalForm(forms.ModelForm):
    class Meta:
        model = DailyGoal
        fields = ['target_calories', 'target_protein', 'target_carbs', 'target_fat']