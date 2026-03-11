from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import UserProfile, DailyGoal
from .forms import UserProfileForm, DailyGoalForm


@login_required
def profile_view(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'profile.html', {'form': form, 'profile': profile})


@login_required
def goals_view(request):
    goal, created = DailyGoal.objects.get_or_create(
        user=request.user,
        defaults={
            'target_calories': 2000,
            'target_protein': 100,
            'target_carbs': 250,
            'target_fat': 70,
        }
    )

    if request.method == 'POST':
        form = DailyGoalForm(request.POST, instance=goal)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = request.user
            goal.save()
            return redirect('goals')
    else:
        form = DailyGoalForm(instance=goal)

    return render(request, 'goals.html', {'form': form, 'goal': goal})