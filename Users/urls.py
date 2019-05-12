from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.login, name='Users-login'),
    path('register/', views.register, name='Users-register'),
]


