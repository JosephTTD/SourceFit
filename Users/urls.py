from . import views
from django.urls import path
from .forms import UserLoginForm

urlpatterns = [
    path('', views.home_view, name='Users-home'),
    path('login/', views.login_view, name='Users-login',),
    path('register/', views.register_view, name='Users-register',),
]


