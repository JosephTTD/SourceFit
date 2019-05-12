from django.shortcuts import render

# Create your views here.
def login(request):
    return render(request, 'Users/login.html', {'title': 'Login'})

def register(request):
    return render(request, 'Users/register.html', {'title': 'Register'})