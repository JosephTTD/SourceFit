from .forms import UserRegisterForm, UserLoginForm
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout


def home_view(request):
    return render(request, 'Users/index.html')

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