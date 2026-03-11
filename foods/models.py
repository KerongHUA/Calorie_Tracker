from django.db import models
from django.contrib.auth.models import User


class FoodCatalogue(models.Model):
    name = models.CharField(max_length=100, unique=True)
    calories_per_100g = models.FloatField()
    protein_per_100g = models.FloatField()
    carbs_per_100g = models.FloatField()
    fat_per_100g = models.FloatField()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.calories_per_100g = round(self.calories_per_100g, 1)
        self.protein_per_100g = round(self.protein_per_100g, 1)
        self.carbs_per_100g = round(self.carbs_per_100g, 1)
        self.fat_per_100g = round(self.fat_per_100g, 1)
        super().save(*args, **kwargs)


class CustomFood(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    calories_per_100g = models.FloatField()
    protein_per_100g = models.FloatField()
    carbs_per_100g = models.FloatField()
    fat_per_100g = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'name')

    def __str__(self):
        return f"{self.name} ({self.user.username})"

    def save(self, *args, **kwargs):
        self.calories_per_100g = round(self.calories_per_100g, 1)
        self.protein_per_100g = round(self.protein_per_100g, 1)
        self.carbs_per_100g = round(self.carbs_per_100g, 1)
        self.fat_per_100g = round(self.fat_per_100g, 1)
        super().save(*args, **kwargs)