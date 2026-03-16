from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('register/', views.register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='auth/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('identify/', views.identify_view, name='identify'),
    path('growth-tips/', views.growth_tips_view, name='growth_tips'),
    path('chatbot/', views.chatbot_view, name='chatbot'),
    path('marketplace/', views.marketplace_view, name='marketplace'),
]
