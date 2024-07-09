from django.urls import path
from . import views


urlpatterns = [
    path('', views.main, name='main'),
    path('appcoworking/', views.users, name='users'),
    path('appcoworking/details/<int:id>', views.details, name='details'),
    path('main/', views.main_view, name='main_view'),
    path('login/', views.user_login, name='login'),
    path('login/', views.user_logout, name='logout'),
    path('registration/', views.registration_view, name='registration'),
    path('testing/', views.testing, name='testing'),
]
