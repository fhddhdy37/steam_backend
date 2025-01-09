from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.conf import settings
import base64

# Create your views here.

def index(request):
    return render(request, 'gpt_api/index.html')

def hi(request):
    return render(request, 'gpt_api/hi.html')

def bye(request):
    data = {
        'name': '김준권',
        'age': 25,
        'is_student': True,
    }
    return JsonResponse(data, json_dumps_params={'ensure_ascii': False})

@csrf_exempt
def hihi(request):
    if request.method == 'POST':
        print(request.POST)
        return JsonResponse({'message': request.POST}, json_dumps_params={'ensure_ascii': False})
    else:
        return JsonResponse({'message': 'POST 요청이 아닙니다.'}, json_dumps_params={'ensure_ascii': False})

def imgtest(request):
    with open(settings.IMAGE_DIR / 'image.png', 'rb') as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    return JsonResponse({'image': encoded_string})