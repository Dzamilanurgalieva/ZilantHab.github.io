from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
import json
from .services.mistral_service import MistralService
from .models import Course, Community, Achievement

mistral_service = MistralService()


def home(request):
    """Главная страница"""
    courses = Course.objects.filter(status='published').order_by('order', '-created_at')
    communities = Community.objects.filter(is_active=True).order_by('order', 'name')
    achievements = Achievement.objects.filter(is_active=True)

    context = {
        'courses': courses,
        'communities': communities,
        'achievements': achievements,
    }
    return render(request, 'index.html', context)


def education(request):
    """Страница обучения"""
    courses = Course.objects.filter(status='published').order_by('order', '-created_at')
    return render(request, 'education.html', {'courses': courses})


def community(request):
    """Страница сообщества"""
    communities = Community.objects.filter(is_active=True).order_by('order', 'name')
    return render(request, 'community.html', {'communities': communities})


def ratings(request):
    """Страница рейтингов"""
    return HttpResponse("Рейтинги учеников - в разработке")


def register_view(request):
    """Страница регистрации"""
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, 'Пароли не совпадают')
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Пользователь с таким именем уже существует')
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Пользователь с таким email уже существует')
            return redirect('register')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1
        )

        login(request, user)
        messages.success(request, 'Регистрация успешно завершена!')
        return redirect('home')

    return render(request, 'register.html')


def login_view(request):
    """Страница входа"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'Добро пожаловать, {user.username}!')
            return redirect('home')
        else:
            messages.error(request, 'Неверное имя пользователя или пароль')

    return render(request, 'login.html')


def logout_view(request):
    """Выход из аккаунта"""
    logout(request)
    messages.success(request, 'Вы вышли из аккаунта')
    return redirect('home')


@login_required
def profile_view(request):
    """Страница профиля пользователя"""
    achievements = Achievement.objects.filter(is_active=True)
    return render(request, 'profile.html', {
        'user': request.user,
        'achievements': achievements
    })


@csrf_exempt
@require_http_methods(["POST"])
def chat_api(request):
    """API для общения с Mistral AI"""
    try:
        data = json.loads(request.body)
        user_message = data.get('message', '').strip()
        conversation_history = data.get('history', [])

        if not user_message:
            return JsonResponse({'error': 'Сообщение не может быть пустым'}, status=400)

        result = mistral_service.get_response(user_message, conversation_history)

        if result['success']:
            return JsonResponse({
                'response': result['response'],
                'history': result['history']
            })
        else:
            return JsonResponse({'error': result['error']}, status=500)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Неверный формат JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': f'Внутренняя ошибка сервера: {str(e)}'}, status=500)


def all_courses(request):
    """Страница со всеми курсами"""
    courses = Course.objects.filter(status='published').order_by('order', '-created_at')
    return render(request, 'courses.html', {'courses': courses})


def all_communities(request):
    """Страница со всеми сообществами"""
    communities = Community.objects.filter(is_active=True).order_by('order', 'name')
    return render(request, 'communities.html', {'communities': communities})