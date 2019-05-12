from django.shortcuts import render

posts = [

    {
        'author' : 'Joe',
        'title' : 'posts',
        'content' : 'succ your dad instead',
        'date_posted' : 'June 17, 2019',
        'current_weight' : '80',
        'goal_weight' : '67',
        'calories_consumed' : '1270',
        'reach_goal' : '81'
    }
]
def dashboard(request):
    context = {
        'posts': posts
    }
    return render(request, 'Core/dashboard.html', context, {})

def profile(request):
    return render(request, 'Core/profile.html', {'title': ''})

def settings(request):
    return render(request, 'Core/settings.html', {'title': 'Settings'})

def diet(request):
    return render(request, 'Core/diet.html', {'title': 'Diet'})

def exercise(request):
    return render(request, 'Core/exercise.html', {'title': 'Exercise'})

def goals(request):
    return render(request, 'Core/goals.html', {'title': 'Goals'})

