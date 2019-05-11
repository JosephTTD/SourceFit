from django.shortcuts import render

posts = [

    {
        'author' : 'joe',
        'title' : 'posts',
        'content' : 'succ your mom',
        'date_posted' : 'June 17, 2019'
    },
    {
        'author': 'berk',
        'title': 'posts2',
        'content': 'succ your mom part 2',
        'date_posted': 'June 18, 2019'
    }
]

def login(request):
    context = {
        'posts': posts
    }
    return render(request, 'Authentication/login.html', context)

def register(request):
    return render(request, 'Authentication/register.html', {'title': 'About'})


