from django.db import models
from django.contrib.auth.models import User
from foods.models import FoodCatalogue, CustomFood


class DailyIntake(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    public_food = models.ForeignKey(
        FoodCatalogue,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    custom_food = models.ForeignKey(
        CustomFood,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    intake_date = models.DateField(auto_now_add=True)
    quantity_grams = models.FloatField()

    calories_consumed = models.FloatField(blank=True, null=True)
    protein_consumed = models.FloatField(blank=True, null=True)
    carbs_consumed = models.FloatField(blank=True, null=True)
    fat_consumed = models.FloatField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def get_selected_food(self):
        return self.public_food or self.custom_food

    def calculate_nutrition(self):
        selected_food = self.get_selected_food()
        if not selected_food:
            return

        self.quantity_grams = round(self.quantity_grams, 1)

        factor = self.quantity_grams / 100
        self.calories_consumed = round(selected_food.calories_per_100g * factor, 1)
        self.protein_consumed = round(selected_food.protein_per_100g * factor, 1)
        self.carbs_consumed = round(selected_food.carbs_per_100g * factor, 1)
        self.fat_consumed = round(selected_food.fat_per_100g * factor, 1)

    def save(self, *args, **kwargs):
        self.calculate_nutrition()
        super().save(*args, **kwargs)

    def __str__(self):
        selected_food = self.get_selected_food()
        food_name = selected_food.name if selected_food else "No food selected"
        return f"{self.user.username} - {food_name} - {self.intake_date}"