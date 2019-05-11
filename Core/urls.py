from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.dashboard, name='Core-dashboard'),
    path('diet/', views.diet, name='Core-diet'),
    path('exercise/', views.exercise, name='Core-exercise'),
    path('profile/', views.profile, name='Core-profile'),
    path('settings/', views.settings, name='Core-settings'),
    path('goals/', views.goals, name='Core-goals'),
]