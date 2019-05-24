from django.template.loader import render_to_string

from .forms import UserRegisterForm, UserLoginForm, GoalCreationForm, DietCreationForm, ActivityCreationForm,\
    WeightModificationForm
from django.contrib import messages
import datetime
from django.shortcuts import render, redirect, render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, get_user_model
from .models import Goal, ExerciseIntensity, DietData, CustomUser, Activity, WeightMeasurementUnits, \
    HeightMeasurementUnits


User = get_user_model()


def home_view(request):
    return render(request, 'Users/index.html')


@login_required(login_url='Users-login')
def dashboard_view(request):
    instance = User.objects.get(username=request.user.username)
    display_name = request.user.username
    f_name = request.user.first_name
    full_name = request.user.get_full_name
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
            'f_name': f_name,
            'full_name' : full_name,
            'display-name' : display_name,
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

    if request.POST and goal is not None:
        if request.method == 'POST':  # If method is GET
            goal.delete()

    if goal is not None:
        goal_completed = goal.check_goal_is_complete(instance.weightUnits, instance.weight)
        goal_exceeded = goal.check_goal_is_expired()

        if goal_exceeded:
            goal.goalExceeded = True
            goal.save()
        elif goal_completed:
            goal.goalCompletion = True
            goal.save()
        # days left till goal deadline
        days_left = goal.return_days_to_goal_deadline()
        goal_weight = goal.goalWeight
        goal_weight_units = goal.weightUnits
        goal_complete = goal.goalCompletion
        goal_exceeded = goal.goalExceeded
    else:
        goal_exceeded = False
        goal_complete = False
        # days left till goal deadline
        days_left = 0
        goal_weight = float(0)
        goal_weight_units = WeightMeasurementUnits.KG.value

    posts = [

        {
            'goal_exceeded': goal_exceeded,
            'goal_completion': goal_complete,
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
    queryset = Activity.objects.filter(user__username=instance.username).values("activityDuration", "activityDistance",
                                                                                "activityName", "typeOfActivity",
                                                                                "completion")

    if request.POST.get('checkboeru', '') == 'on':
            print("CHECKHIT")

    context = {
        'queryset': queryset
    }
    return render(request, "Users/exercise.html", context)


@login_required(login_url='Users-login')
def display_diet_view(request):
    instance = User.objects.get(username=request.user.username)
    date_from = datetime.datetime.now() - datetime.timedelta(days=1)
    maintenance_calories = instance.calculate_maintenance_calories()
    queryset = DietData.objects.filter(user__username=instance.username).values("calorificCount", "dateAdded", "foodOrDrinkName", "typeOfMeal")
    queryAllDailyCalories = DietData.objects.filter(user__username=instance.username,
                                                    dateAdded__gte=date_from).values_list('calorificCount',flat=True)
    dailyCalories = 0
    for i in queryAllDailyCalories:
        dailyCalories += i
    context = {
        'queryset': queryset,
        'dailyCalories': dailyCalories,
        'maintenance_calories': maintenance_calories
    }

    return render(request, "Users/diet.html", context)


@login_required(login_url='Users-login')
def create_goal_view(request):
    instance = User.objects.get(username=request.user.username)
    if request.method == 'POST' and Goal:
        form = GoalCreationForm(request.POST)
        if form.is_valid():
            if Goal.objects.filter(user__username=instance.username).exists():
                return redirect('Users-goals')
            else:
                post = form.save(commit=False)
                post.user = instance
                post.save()
                return redirect('Users-goals')
    else:
        form = GoalCreationForm()
    return render(request, 'Users/goal_entry.html', {'form': form},)


@login_required(login_url='Users-login')
def create_diet_view(request):
    instance = User.objects.get(username=request.user.username)
    if request.method == 'POST':
        form = DietCreationForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = instance
            post.save()
            return redirect('Users-diet')
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
            return redirect('Users-dashboard')
    else:
        form = UserLoginForm()
    return render(request, 'Users/login.html', {'form': form})


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('Users-login')

######place form into PROFILE.HTML
def profile(request):
    instance = User.objects.get(username=request.user.username)
    if request.method == 'POST':
        form = WeightModificationForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = instance
            post.save()
    else:
        form = WeightModificationForm()

    display_name = request.user.username
    full_name = request.user.get_full_name
    maintenance_calories = instance.calculate_maintenance_calories()
    current_weight = instance.weight
    user_weight_units = instance.weightUnits
    date_from = datetime.datetime.now() - datetime.timedelta(days=1)
    queryAllDailyCalories = DietData.objects.filter(user__username=instance.username,
                                                    dateAdded__gte=date_from).values_list('calorificCount',flat=True)
    dailyCalories = 0
    for i in queryAllDailyCalories:
        dailyCalories += i
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
            'full_name' : full_name,
            'display_name' : display_name,
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
        'dailyCalories' : dailyCalories,
        'posts': posts,
        'form': form
    }
    return render(request, 'Users/profile.html', context)