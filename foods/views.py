from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import FoodCatalogue, CustomFood
from .forms import CustomFoodForm


@login_required
def food_list_view(request):
    public_foods = FoodCatalogue.objects.all().order_by('name')
    custom_foods = CustomFood.objects.filter(user=request.user).order_by('name')

    return render(request, 'food_list.html', {
        'public_foods': public_foods,
        'custom_foods': custom_foods,
    })


@login_required
def add_custom_food_view(request):
    if request.method == 'POST':
        form = CustomFoodForm(request.POST, user=request.user)
        if form.is_valid():
            food = form.save(commit=False)
            food.user = request.user
            food.save()
            return redirect('food_list')
    else:
        form = CustomFoodForm(user=request.user)

    return render(request, 'add_custom_food.html', {'form': form})