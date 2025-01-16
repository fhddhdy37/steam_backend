from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.forms.models import model_to_dict
from .gpt_test import get_keyword_from_diary, get_image
from django.conf import settings
import base64
import json
from .models import Diary
from pprint import pprint
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import DataSerializer



# Create your views here.

class DataList(APIView):
    def get(self, request):
        data = Data.objects.all()
        serializer = DataSerializer(data, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = DataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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

@ensure_csrf_cookie
def get_csrf(request):
    csrf_token = request.META.get('CSRF_COOKIE', None)
    return JsonResponse({'csrfToken': csrf_token}, json_dumps_params={'ensure_ascii': False})

@csrf_exempt
def get_keyword(request):
    if request.method == 'POST':
        keyword = get_keyword_from_diary()
        image_path = get_image(keyword)
        if image_path:
            return JsonResponse({'keyword': keyword, 'image_path': image_path}, json_dumps_params={'ensure_ascii': False})
        else:
            return JsonResponse({'keyword': keyword, 'error': '이미지 생성 실패'}, json_dumps_params={'ensure_ascii': False})
    else:
        return JsonResponse({'error': 'POST 요청이 아닙니다.'}, json_dumps_params={'ensure_ascii': False})

def imgtest(request):
    return render(request, 'gpt_api/imgtest.html', {'IMAGE_URL': settings.IMAGE_URL})

def imgtest(request):
    with open(settings.IMAGE_DIR / 'image.png', 'rb') as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    return JsonResponse({'image': encoded_string})

def dbtest(request):
    return render(request, 'gpt_api/dbtest.html')

@csrf_exempt
def diary(request):
    if request.method == 'POST':
        body_data = json.loads(request.body.decode('utf-8'))
        print(body_data.get('content'))
        return JsonResponse({'message': 'POST 요청 성공', 'content': body_data.get('content')}, json_dumps_params={'ensure_ascii': False})
    else:
        return JsonResponse({'message': 'POST 요청이 아닙니다.'}, json_dumps_params={'ensure_ascii': False})

@csrf_exempt
def add_test_data(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        diary = Diary.objects.create(
            title=data['title'],
            content=data['content'],
            date=data['date'],
            sticker_path=data['sticker_path']
        )
        return JsonResponse({'message': 'Data added successfully', 'diary': {
            'title': diary.title,
            'content': diary.content,
            'date': diary.date,
            'sticker_path': diary.sticker_path
        }})
    return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
def delete_all_data(request):
    if request.method == 'POST':
        Diary.objects.all().delete()
        return JsonResponse({'message': 'All data deleted successfully'})
    return JsonResponse({'error': 'Invalid request'}, status=400)

def get_diary_content(request):
    if request.method == 'GET':
        diary = list(Diary.objects.all().values('title', 'content', 'date'))
        return JsonResponse({'diary': diary})
    return JsonResponse({'error': 'Invalid request'}, status=400)

def get_diary_content2(request):
    if request.method == 'GET':
        diary_entries = Diary.objects.all()
        diary_list = [model_to_dict(entry) for entry in diary_entries]
        return JsonResponse({'diary': diary_list[0]})
    return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
def get_today_diary(request):
    if request.method == 'POST':
        body_data = json.loads(request.body.decode('utf-8'))
        date = body_data.get('date')
        print(date)
        diary_entry = Diary.objects.filter(date=date).first()
        print(diary_entry)
        diary = model_to_dict(diary_entry)
        return JsonResponse({'content': diary.get('content')})
    
@csrf_exempt
def report_diary(request):
    if request.method == 'POST':
        try:
            body_data = json.loads(request.body.decode('utf-8'))
            diary_data = body_data.get('diary')
            if not diary_data:
                return JsonResponse({'error': 'Diary data not provided'}, status=400)
            
            diary = Diary.objects.create(
                title=diary_data.get('title'),
                content=diary_data.get('content'),
                date=diary_data.get('date'),
                sticker_path='images/sticker.png'
            )
            diary_dict = model_to_dict(diary)
            return JsonResponse({'message': 'Diary saved successfully', 'diary': diary_dict}, json_dumps_params={'ensure_ascii': False})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    return JsonResponse({'error': 'Invalid request'}, status=400)
