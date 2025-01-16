from rest_framework import serializers
from .models import Diary

#데이터를 JSON 형식으로 변환환
class DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diary
        fields = '__all__'
