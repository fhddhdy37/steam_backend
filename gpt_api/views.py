import base64

from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from rest_framework.views import APIView

from .models import Diary
from .gpt_test import generate_image, generate_keyword_from_diary
from .serializers import DiarySerializer

# Create your views here.

#클래스명 변경 필요: 의미에 맞지 않는듯
class DataList(APIView):
    def get(self, request):
        data = request.data
        date = data.get('date')
        if date:
            diary_entries = Diary.objects.filter(date=date).first()
            if not diary_entries:
                return JsonResponse({'error': 'Data not found'}, status=404)
            serializer = DiarySerializer(diary_entries)
            return JsonResponse({'data': serializer.data}, safe=False)
        else:
            return JsonResponse({'error': 'Invalid request'}, status=400)

    def post(self, request):
        data = request.data
        try:
            title = data.get('title')
            content = data.get('content')
            keyword = generate_keyword_from_diary(content)
            sticker_path = generate_image(keyword)
            date = data.get('date')

            diary = Diary.objects.create(title=title, content=content, date=date, sticker_path=sticker_path)
            return JsonResponse({'message': 'Data added successfully', 'diary': {
                'title': diary.title,
                'content': diary.content,
                'date': diary.date,
                'sticker_path': diary.sticker_path
            }})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
#클라이언트에 이미지 띄워주는 테스트 함수
def imgtest(request):
    with open(settings.IMAGE_DIR / 'image.png', 'rb') as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    return JsonResponse({'image': encoded_string})
