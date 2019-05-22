from .forms import UserRegisterForm, UserLoginForm, GoalCreationForm
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, get_user_model
from .models import Goal, ExerciseIntensity, DietData, CustomUser, Activity

User = get_user_model()


def home_view(request):
    return render(request, 'Users/index.html')


@login_required(login_url='Users-login')
def dashboard_view(request):
    instance = User.objects.get(username=request.user.username)
    maintenance_calories = instance.calculate_maintenance_calories()
    current_weight = instance.weight
    user_weight_units = instance.weightUnits
    #boolean whether goal is complete or not
    goal = Goal.objects.get(goal__username=instance.username)
    goal_complete = goal.check_goal_is_complete(instance.weightUnits, instance.weight)
    #days left till goal deadline
    days_left = goal.return_days_to_goal_deadline()
    goal_weight = goal.goalWeight
    goal_weight_units = goal.weightUnits

    context = {
        'maintenance_calories': maintenance_calories,
        'user_weight': current_weight,
        'user_weight_units': user_weight_units,
        'goal_complete': goal_complete,
        'days_left': days_left,
        'goal_weight': goal_weight,
        'goal_weight_units': goal_weight_units,
    }
    return render(request, 'Users/dashboard.html', context=context)


@login_required(login_url='Users-login')
def display_goal_view(request):
    instance = User.objects.get(goal__username=request.user.username)
    goal = Goal.objects.get(goal__username=instance.username)
    goal_complete = goal.check_goal_is_complete(instance.weightUnits, instance.weight)
    days_left = goal.return_days_to_goal_deadline()
    goal_weight = goal.goalWeight
    goal_weight_units = goal.weightUnits
    context = {
        'goal_complete': goal_complete,
        'days_left': days_left,
        'goal_weight': goal_weight,
        'goal_weight_units': goal_weight_units,
    }
    return render(request, 'Users/dashboard.html', context=context)


@login_required(login_url='Users-login')
def display_exercise_view(request):
    instance = User.objects.get(activity__username=request.user.username)
    queryset = Activity.objects.filter(activity__username=instance.username)
    context = {
        "Exercise_object_list": queryset
    }
    return render(request, "Users/exercise.html", context)


@login_required(login_url='Users-login')
def display_diet_view(request):
    instance = User.objects.get(diet__username=request.user.username)
    queryset = DietData.objects.filter(diet__username=instance.username)
    context = {
        "Diet_object_list": queryset
    }
    return render(request, "Users/diet.html", context)


@login_required(login_url='Users-login')
def create_goal_view(request):
    if request.method == 'POST':
        form = GoalCreationForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = GoalCreationForm()
    return render(request, 'Users/goals.html', {'form': form})


@login_required(login_url='Users-login')
def create_diet_view(request):
    if request.method == 'POST':
        form = GoalCreationForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = GoalCreationForm()
    return render(request, 'Users/diet.html', {'form': form})


@login_required(login_url='Users-login')
def create_exercise_view(request):
    if request.method == 'POST':
        form = GoalCreationForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = GoalCreationForm()
    return render(request, 'Users/exercise.html', {'form': form})


def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}.')
            return redirect('Users-login')
    else:
        form = UserRegisterForm()
    return render(request, 'Users/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            # log in
            user = form.get_user()
            login(request, user, backend='Users.auth.EmailOrUsernameModelBackend')
            return redirect('Users-login')
    else:
        form = UserLoginForm()
    return render(request, 'Users/login.html', {'form': form})


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('/Users/login.html')

posts = [

    {
        'author' : 'Joe',
        'title' : 'posts',
        'content' : 'succ your dad instead',
        'date_posted' : 'June 17, 2019',
        'current_weight' : '80',
        'goal_weight' : '67',
        'calories_consumed' : '1270',
        'reach_goal' : '81',
        'First_name' : 'Joseph',
        'Second_name' : 'Dada'
    }
]
def dashboard(request):
    context = {
        'posts': posts
    }
    return render(request, 'Users/dashboard.html', context, {})

def profile(request):
    context = {
        'posts': posts
    }
    return render(request, 'Users/profile.html', context, {'title': 'Profile'})

def settings(request):
    context = {
        'posts' : posts
    }
    return render(request, 'Users/settings.html', context, {'title': 'Settings'})

def diet(request):
    context = {
        'posts': posts
    }
    return render(request, 'Users/diet.html', context, {'title': 'Diet'})

def exercise(request):
    context = {
        'posts': posts
    }
    return render(request, 'Users/exercise.html', context, {'title': 'Exercise'})

def goals(request):
    context = {
        'posts': posts
    }

    return render(request, 'Users/goals.html', context, {'title': 'Goals'})