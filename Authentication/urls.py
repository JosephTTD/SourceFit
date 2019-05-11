from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='Authentication-login'),
    path('register/', views.register, name='Authentication-register'),
]