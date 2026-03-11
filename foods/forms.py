from django import forms
from .models import CustomFood, FoodCatalogue


class CustomFoodForm(forms.ModelForm):
    class Meta:
        model = CustomFood
        fields = [
            'name',
            'calories_per_100g',
            'protein_per_100g',
            'carbs_per_100g',
            'fat_per_100g',
        ]

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean_name(self):
        name = self.cleaned_data['name'].strip()

        if FoodCatalogue.objects.filter(name__iexact=name).exists():
            raise forms.ValidationError(
                'This food already exists in the public food catalogue.'
            )

        if self.user and CustomFood.objects.filter(user=self.user, name__iexact=name).exists():
            raise forms.ValidationError(
                'You already created a custom food with this name.'
            )

        return name