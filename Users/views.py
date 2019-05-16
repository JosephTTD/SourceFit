from .forms import UserRegisterForm
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout


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
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            # log in
            user = form.get_user()
            login(request, user, backend='Users.auth.EmailOrUsernameModelBackend')
            return redirect('Users-login')
    else:
        form = AuthenticationForm()
    return render(request, 'Users/login.html', {'form': form})


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('/Users/login.html')