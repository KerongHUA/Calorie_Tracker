from django import forms
from .models import DailyIntake
from foods.models import FoodCatalogue, CustomFood


class DailyIntakeForm(forms.ModelForm):
    food_choice = forms.ChoiceField(
        choices=[],
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = DailyIntake
        fields = ['food_choice', 'quantity_grams']
        widgets = {
            'quantity_grams': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0.1',
                'step': '0.1',
            })
        }

    def __init__(self, *args, user=None, **kwargs):
        instance = kwargs.get('instance')
        super().__init__(*args, **kwargs)
        self.user = user

        public_foods = FoodCatalogue.objects.all().order_by('name')
        custom_foods = CustomFood.objects.filter(user=user).order_by('name') if user else []

        public_choices = [
            (
                f'public_{food.id}',
                (
                    f"{food.name} "
                    f"({food.calories_per_100g:.1f} kcal, "
                    f"P {food.protein_per_100g:.1f}g, "
                    f"C {food.carbs_per_100g:.1f}g, "
                    f"F {food.fat_per_100g:.1f}g / 100g)"
                )
            )
            for food in public_foods
        ]

        custom_choices = [
            (
                f'custom_{food.id}',
                (
                    f"{food.name} "
                    f"({food.calories_per_100g:.1f} kcal, "
                    f"P {food.protein_per_100g:.1f}g, "
                    f"C {food.carbs_per_100g:.1f}g, "
                    f"F {food.fat_per_100g:.1f}g / 100g)"
                )
            )
            for food in custom_foods
        ]

        choices = []

        if public_choices:
            choices.append(('Public Foods', public_choices))

        if custom_choices:
            choices.append(('My Custom Foods', custom_choices))

        self.fields['food_choice'].choices = choices

        if instance:
            if instance.public_food:
                self.fields['food_choice'].initial = f'public_{instance.public_food.id}'
            elif instance.custom_food:
                self.fields['food_choice'].initial = f'custom_{instance.custom_food.id}'

    def clean(self):
        cleaned_data = super().clean()
        food_choice = cleaned_data.get('food_choice')

        if not food_choice:
            raise forms.ValidationError('Please choose one food.')

        return cleaned_data