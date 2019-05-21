from . import views
from django.urls import path
from .forms import UserLoginForm

urlpatterns = [
    path('', views.home_view, name='Users-home'),
    path('login/', views.login_view, name='Users-login',),
    path('register/', views.register_view, name='Users-register',),
    path('dashboard/', views.dashboard, name='Users-dashboard'),
    path('diet/', views.diet, name='Users-diet'),
    path('exercise/', views.exercise, name='Users-exercise'),
    path('profile/', views.profile, name='Users-profile'),
    path('settings/', views.settings, name='Users-settings'),
    path('goals/', views.goals, name='Users-goals'),
]


