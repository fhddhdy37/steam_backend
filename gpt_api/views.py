from django.shortcuts import render
from django.http import JsonResponse

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