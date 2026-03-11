from datetime import date
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.db.models import Sum
from .forms import RegisterForm
from intake.models import DailyIntake
from profiles.models import DailyGoal


def home(request):
    if not request.user.is_authenticated:
        return render(request, 'home.html')

    today = date.today()

    intakes = DailyIntake.objects.filter(
        user=request.user,
        intake_date=today
    ).order_by('-created_at')

    today_totals = intakes.aggregate(
        total_calories=Sum('calories_consumed'),
        total_protein=Sum('protein_consumed'),
        total_carbs=Sum('carbs_consumed'),
        total_fat=Sum('fat_consumed'),
    )

    total_calories = today_totals['total_calories'] or 0
    total_protein = today_totals['total_protein'] or 0
    total_carbs = today_totals['total_carbs'] or 0
    total_fat = today_totals['total_fat'] or 0

    goal = DailyGoal.objects.filter(user=request.user).first()

    target_calories = goal.target_calories if goal else 0
    target_protein = goal.target_protein if goal else 0
    target_carbs = goal.target_carbs if goal else 0
    target_fat = goal.target_fat if goal else 0

    remaining_calories = target_calories - total_calories

    context = {
        'today': today,
        'intakes': intakes,
        'total_calories': total_calories,
        'total_protein': total_protein,
        'total_carbs': total_carbs,
        'total_fat': total_fat,
        'target_calories': target_calories,
        'target_protein': target_protein,
        'target_carbs': target_carbs,
        'target_fat': target_fat,
        'remaining_calories': remaining_calories,
    }

    return render(request, 'dashboard.html', context)

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})


def login_view(request):
    error_message = None

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            error_message = 'Invalid username or password'

    return render(request, 'login.html', {'error_message': error_message})


def logout_view(request):
    logout(request)
    return redirect('home')