import base64

from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from rest_framework.views import APIView

from .models import Diary
from .gpt_test import generate_image, generate_keyword_from_diary
from .serializers import DiarySerializer

# Create your views here.

class GetDiary(APIView):
    def get(self, request):
        '''
            endpoint: /getdiary/
            일기 데이터를 가져오는 API
            
            query params: none
            response body:
            {
                "diary": [
                    {
                        "id": number,
                        "title": "제목",
                        "content": "본문",
                        "keywords": "일기 핵심 키워드",
                        "sticker_path": "이미지 경로",
                        "date": "YYYY-MM-DD"
                        "is_favorite": boolean
                    },
                    ...
                ]
            }


            query params:
            {
                "date": "YYYY-MM-DD"
            }

            response body:
            {
                "diary": {
                    "id": number,
                    "title": "제목",
                    "content": "본문",
                    "keywords": "일기 핵심 키워드",
                    "sticker_path": "이미지 경로",
                    "date": "YYYY-MM-DD"
                    "is_favorite": boolean
                }
            }
        '''

        date = request.query_params.get('date')
        if date:
            diary_entries = Diary.objects.filter(date=date).first()
            if not diary_entries:
                return JsonResponse({'error': 'Data not found'}, status=404)
            serializer = DiarySerializer(diary_entries)
        else:
            diary_entries = Diary.objects.all()
            serializer = DiarySerializer(diary_entries, many=True)

        return JsonResponse({'diary': serializer.data}, json_dumps_params={'ensure_ascii': False})

class PostDiary(APIView):
    def post(self, request):
        '''
            endpoint: /postdiary/
            일기 데이터를 등록하는 API

            로그인 기능 구현 이후 request.user로 username을 가져오도록 수정

            request body:
            {
                "title": "제목", (required)
                "content": "본문", (required)
                "date": "YYYY-MM-DD" (required)
            }

            response body:
            {
                "message": "Data added successfully",
                "diary": {
                    "id": number,
                    "title": "제목",
                    "content": "본문",
                    "keywords": "일기 핵심 키워드",
                    "sticker_path": "이미지 경로",
                    "date": "YYYY-MM-DD"
                }
            }
        '''

        data = request.data
        try:
            # 로그인 구현 이후 username을 세션에서 가져오도록 수정
            username = "testuser"
            title = data.get('title')
            content = data.get('content')
            keyword = generate_keyword_from_diary(content)
            sticker_path = generate_image(keyword, username)
            date = data.get('date')

            diary = Diary.objects.create(title=title, content=content, keywords=keyword, sticker_path=sticker_path, date=date)
            return JsonResponse({'message': 'Data added successfully', 'diary': {
                'id': diary.id,
                # 'user_id': diary.user_id,
                'title': diary.title,
                'content': diary.content,
                'keyword': diary.keywords,
                'sticker_path': diary.sticker_path,
                'date': diary.date
            }})
        except Exception as e:
            print(e)
            return JsonResponse({'error': str(e)}, status=400)

class GetImage(APIView):
    def get(self, request):
        '''
            endpoint: /getimage/
            이미지 데이터를 가져오는 API

            query params:
            {
                "user_id": "유저 아이디",
                "sticker_path": "이미지 경로"
            }

            response body:
            {
                "image": "이미지 데이터"
            }
        '''

        # user_id = request.data.get('user_id')
        user_id = 'testuser'
        sticker_path = request.query_params.get('sticker_path')
        sticker_path = sticker_path.split('/')[-1]
        with open(settings.IMAGE_DIR / f"{user_id}/{sticker_path}", 'rb') as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        return JsonResponse({'image': encoded_string})
    
#클라이언트에 이미지 띄워주는 테스트 함수
def imgtest(request):
    with open(settings.IMAGE_DIR / 'image.png', 'rb') as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    return JsonResponse({'image': encoded_string})
