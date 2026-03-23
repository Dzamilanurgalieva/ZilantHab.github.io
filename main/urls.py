from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('education/', views.education, name='education'),
    path('community/', views.community, name='community'),
    path('ratings/', views.ratings, name='ratings'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
]