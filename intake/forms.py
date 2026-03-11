from django import forms
from .models import DailyIntake
from foods.models import FoodCatalogue, CustomFood


class DailyIntakeForm(forms.ModelForm):
    food_choice = forms.ChoiceField(choices=[])

    class Meta:
        model = DailyIntake
        fields = ['food_choice', 'quantity_grams']

    def __init__(self, *args, user=None, **kwargs):
        instance = kwargs.get('instance')
        super().__init__(*args, **kwargs)
        self.user = user

        public_foods = FoodCatalogue.objects.all().order_by('name')
        custom_foods = CustomFood.objects.filter(user=user).order_by('name') if user else []

        public_choices = [
            (f'public_{food.id}', food.name)
            for food in public_foods
        ]

        custom_choices = [
            (f'custom_{food.id}', food.name)
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