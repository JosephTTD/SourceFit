from . import views
from django.urls import path
from .forms import UserLoginForm

urlpatterns = [
    path('', views.home_view, name='Users-home'),
    path('login/', views.login_view, name='Users-login',),
    path('register/', views.register_view, name='Users-register',),
    path('dashboard/', views.dashboard_view, name='Users-dashboard'),
    path('diet/', views.display_diet_view, name='Users-diet'),
    path('diet/add_diet', views.create_diet_view, name='Users-add_diet'),
    path('exercise/', views.display_exercise_view, name='Users-exercise'),
    path('exercise/add_exercise/', views.create_exercise_view, name='Users-add_exercise'),
    path('profile/', views.profile, name='Users-profile'),
    path('goals/', views.display_goal_view, name='Users-goals'),
    path('goals/goal_entry/', views.create_goal_view, name='Users-goal_entry'),
]
