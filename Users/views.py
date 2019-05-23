from .forms import UserRegisterForm, UserLoginForm, GoalCreationForm, DietCreationForm, ActivityCreationForm
from django.contrib import messages
import datetime
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, get_user_model
from .models import Goal, ExerciseIntensity, DietData, CustomUser, Activity, WeightMeasurementUnits


User = get_user_model()


def home_view(request):
    return render(request, 'Users/index.html')


@login_required(login_url='Users-login')
def dashboard_view(request):
    instance = User.objects.get(username=request.user.username)
    print(instance.weight)
    maintenance_calories = instance.calculate_maintenance_calories()
    current_weight = instance.weight
    user_weight_units = instance.weightUnits
    #boolean whether goal is complete or not
    try:
        goal = Goal.objects.get(user__username=instance.username)
    except Goal.DoesNotExist:
        goal = None
    if goal is not None:
        goal_complete = goal.check_goal_is_complete(instance.weightUnits, instance.weight)
        # days left till goal deadline
        days_left = goal.return_days_to_goal_deadline()
        goal_weight = goal.goalWeight
        goal_weight_units = goal.weightUnits
    else:
        goal_complete = False
        # days left till goal deadline
        days_left = 0
        goal_weight = float(0)
        goal_weight_units = WeightMeasurementUnits.KG

    posts = [

        {
            'goal_complete': goal_complete,
            'days_left': days_left,
            'goal_weight': goal_weight,
            'goal_weight_units': goal_weight_units,
            'maintenance_calories': maintenance_calories,
            'current_weight': current_weight,
            'user_weight_units': user_weight_units
        }
    ]

    context = {
        'posts': posts
    }
    return render(request, 'Users/dashboard.html', context)


@login_required(login_url='Users-login')
def display_goal_view(request):
    instance = User.objects.get(username=request.user.username)
    try:
        goal = Goal.objects.get(user__username=instance.username)
    except Goal.DoesNotExist:
        goal = None

    if goal is not None:
        goal_complete = goal.check_goal_is_complete(instance.weightUnits, instance.weight)
        # days left till goal deadline
        days_left = goal.return_days_to_goal_deadline()
        goal_weight = goal.goalWeight
        goal_weight_units = goal.weightUnits
    else:
        goal_complete = False
        # days left till goal deadline
        days_left = 0
        goal_weight = float(0)
        goal_weight_units = WeightMeasurementUnits.KG.value
    posts = [

        {
            'goal_complete': goal_complete,
            'days_left': days_left,
            'goal_weight': goal_weight,
            'goal_weight_units': goal_weight_units,
        }
    ]

    context = {
        'posts': posts
    }
    return render(request, 'Users/goals.html', context)


@login_required(login_url='Users-login')
def display_exercise_view(request):
    instance = User.objects.get(username=request.user.username)
    queryset = Activity.objects.filter(user__username=instance.username)
    context = {
        'posts' : posts
    }
    return render(request, "Users/exercise.html", context)


@login_required(login_url='Users-login')
def display_diet_view(request):
    instance = User.objects.get(username=request.user.username)
    date_from = datetime.datetime.now() - datetime.timedelta(days=1)
    queryset = DietData.objects.filter(user__username=instance.username, dateAdded__gte=date_from)
    context = {
        "posts": queryset
    }

    testdata = {
        'posts':posts
    }

    return render(request, "Users/diet.html", testdata, context)


@login_required(login_url='Users-login')
def create_goal_view(request):
    instance = User.objects.get(username=request.user.username)
    if request.method == 'POST':
        form = GoalCreationForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = instance
            post.save()
            redirect('/Users/goals.html')
    else:
        form = GoalCreationForm()
    return render(request, 'Users/goal_entry.html', {'form': form})


@login_required(login_url='Users-login')
def create_diet_view(request):
    instance = User.objects.get(username=request.user.username)
    if request.method == 'POST':
        form = DietCreationForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = instance
            post.save()
            return redirect('/Users/diet.html')
    else:
        form = DietCreationForm()
    return render(request, 'Users/add_diet.html', {'form': form})


@login_required(login_url='Users-login')
def create_exercise_view(request):
    instance = User.objects.get(username=request.user.username)
    if request.method == 'POST':
        form = ActivityCreationForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = instance
            post.save()
            return redirect('Users-exercise')
    else:
        form = ActivityCreationForm()
    return render(request, 'Users/exercise_entry.html', {'form': form})


def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}.')
            return redirect('/Users/login.html')
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
            return redirect('Users-dashboard')
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

def profile(request):
    context = {
        'posts': posts
    }
    return render(request, 'Users/profile.html', context, {'title': 'Profile'})

def goal_entry(request):
    context = {
        'posts' : posts
    }
    return render(request, 'Users/goal_entry.html', context, {'title': ''})

def add_exercise(request):
    context = {
        'posts' : posts
    }
    return render(request, 'Users/exercise_entry.html', context, {'title': ''})

def add_diet(request):
    context = {
        'posts' : posts
    }
    return render(request, 'Users/add_diet.html', context, {'title': ''})

'''
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
    
def dashboard(request):
    context = {
        'posts': posts
    }
    return render(request, 'Users/dashboard.html', context, {})
'''