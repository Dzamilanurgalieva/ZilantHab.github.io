from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('education/', views.education, name='education'),
    path('community/', views.community, name='community'),
    path('ratings/', views.ratings, name='ratings'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('api/chat/', views.chat_api, name='chat_api'),
    path('courses/', views.all_courses, name='all_courses'),
    path('communities/', views.all_communities, name='all_communities'),
]