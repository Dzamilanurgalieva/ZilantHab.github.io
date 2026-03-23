from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    """Главная страница"""
    return render(request, 'index.html')

def education(request):
    """Страница обучения"""
    return render(request, 'index.html')  # временно показывает главную

def community(request):
    """Страница сообщества"""
    return HttpResponse("Сообщество - в разработке")

def ratings(request):
    """Страница рейтингов"""
    return HttpResponse("Рейтинги учеников - в разработке")

def login_view(request):
    """Страница входа"""
    return HttpResponse("Страница входа - в разработке")

def register_view(request):
    """Страница регистрации"""
    return HttpResponse("Страница регистрации - в разработке")