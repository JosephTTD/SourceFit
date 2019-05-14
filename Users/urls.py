from . import views
from django.urls import path

urlpatterns = [
    path('', views.login_view, name='Users-login'),
    path('register/', views.register_view, name='Users-register'),
]


