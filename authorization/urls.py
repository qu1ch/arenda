from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'authorization'

urlpatterns = [
    path('', views.login_view, name='login'),
    path('register', views.register, name='register'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

]
