from django.contrib import admin
from .models import UserProfile, DailyGoal

admin.site.register(UserProfile)
admin.site.register(DailyGoal)