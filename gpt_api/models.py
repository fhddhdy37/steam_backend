from django.db import models

# Create your models here.

class User(models.Model):
    '''
        유저 정보를 저장하는 모델
        
        nickname: 유저의 닉네임
        id: 유저의 아이디
        password: 유저의 비밀번호
        password는 해싱하여 저장할 예정 (import hashlib)
    '''
    nickname = models.CharField(max_length=15)
    id = models.CharField(max_length=20, primary_key=True)
    password = models.CharField(max_length=20)

class Diary(models.Model):
    '''
        일기 정보를 저장하는 모델

        id: 일기의 고유 아이디
        user_id: 일기를 작성한 유저의 아이디
        title: 일기의 제목
        content: 일기의 내용
        keywords: 일기의 키워드
        sticker_path: 일기에 대한 스티커 이미지 경로
        date: 일기의 작성 날짜
        is_favorite: 즐겨찾기 여부
    '''
    id = models.AutoField(primary_key=True)
    # user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    content = models.TextField()
    keywords = models.CharField(max_length=100)
    sticker_path = models.CharField(max_length=100, null=True)
    date = models.DateField()
    is_favorite = models.BooleanField(default=False)