from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from .services.mistral_service import MistralService

# Инициализируем сервис один раз
mistral_service = MistralService()


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


# API эндпоинт для чата с Mistral AI
@csrf_exempt
@require_http_methods(["POST"])
def chat_api(request):
    """API для общения с Mistral AI"""
    try:
        # Получаем данные из запроса
        data = json.loads(request.body)
        user_message = data.get('message', '').strip()
        conversation_history = data.get('history', [])

        # Проверяем, что сообщение не пустое
        if not user_message:
            return JsonResponse({'error': 'Сообщение не может быть пустым'}, status=400)

        # Получаем ответ от Mistral AI
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