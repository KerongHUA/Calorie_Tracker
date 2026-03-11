from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import DailyIntake
from .forms import DailyIntakeForm
from foods.models import FoodCatalogue, CustomFood
from django.db.models import Sum
from datetime import datetime


@login_required
def add_intake_view(request):
    if request.method == 'POST':
        form = DailyIntakeForm(request.POST, user=request.user)
        if form.is_valid():
            intake = DailyIntake(
                user=request.user,
                quantity_grams=form.cleaned_data['quantity_grams']
            )

            food_choice = form.cleaned_data['food_choice']

            if food_choice.startswith('public_'):
                food_id = int(food_choice.split('_')[1])
                intake.public_food = FoodCatalogue.objects.get(id=food_id)
                intake.custom_food = None

            elif food_choice.startswith('custom_'):
                food_id = int(food_choice.split('_')[1])
                intake.custom_food = CustomFood.objects.get(id=food_id, user=request.user)
                intake.public_food = None

            intake.save()
            return redirect('intake_list')
    else:
        form = DailyIntakeForm(user=request.user)

    return render(request, 'add_intake.html', {'form': form})


@login_required
def intake_list_view(request):
    intakes = DailyIntake.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'intake_list.html', {'intakes': intakes})


@login_required
def edit_intake_view(request, intake_id):
    intake = get_object_or_404(DailyIntake, id=intake_id, user=request.user)

    if request.method == 'POST':
        form = DailyIntakeForm(request.POST, user=request.user, instance=intake)
        if form.is_valid():
            intake.quantity_grams = form.cleaned_data['quantity_grams']

            food_choice = form.cleaned_data['food_choice']

            if food_choice.startswith('public_'):
                food_id = int(food_choice.split('_')[1])
                intake.public_food = FoodCatalogue.objects.get(id=food_id)
                intake.custom_food = None

            elif food_choice.startswith('custom_'):
                food_id = int(food_choice.split('_')[1])
                intake.custom_food = CustomFood.objects.get(id=food_id, user=request.user)
                intake.public_food = None

            intake.save()
            return redirect('intake_list')
    else:
        form = DailyIntakeForm(user=request.user, instance=intake)

    return render(request, 'edit_intake.html', {'form': form, 'intake': intake})


@login_required
def delete_intake_view(request, intake_id):
    intake = get_object_or_404(DailyIntake, id=intake_id, user=request.user)

    if request.method == 'POST':
        intake.delete()
        return redirect('intake_list')

    return render(request, 'delete_intake.html', {'intake': intake})

@login_required
def intake_history_view(request):
    history = (
        DailyIntake.objects
        .filter(user=request.user)
        .values('intake_date')
        .annotate(
            total_calories=Sum('calories_consumed'),
            total_protein=Sum('protein_consumed'),
            total_carbs=Sum('carbs_consumed'),
            total_fat=Sum('fat_consumed'),
        )
        .order_by('-intake_date')
    )

    return render(request, 'intake_history.html', {'history': history})


@login_required
def intake_history_detail_view(request, intake_date):
    selected_date = datetime.strptime(intake_date, '%Y-%m-%d').date()

    intakes = DailyIntake.objects.filter(
        user=request.user,
        intake_date=selected_date
    ).order_by('-created_at')

    totals = intakes.aggregate(
        total_calories=Sum('calories_consumed'),
        total_protein=Sum('protein_consumed'),
        total_carbs=Sum('carbs_consumed'),
        total_fat=Sum('fat_consumed'),
    )

    context = {
        'selected_date': selected_date,
        'intakes': intakes,
        'total_calories': totals['total_calories'] or 0,
        'total_protein': totals['total_protein'] or 0,
        'total_carbs': totals['total_carbs'] or 0,
        'total_fat': totals['total_fat'] or 0,
    }

    return render(request, 'intake_history_detail.html', context)