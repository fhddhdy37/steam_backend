from django.db import models

# Create your models here.

class User(models.Model):
    nickname = models.CharField(max_length=15)
    id = models.CharField(max_length=20, primary_key=True)
    password = models.CharField(max_length=20)

class Diary(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    content = models.TextField()
    keywords = models.CharField(max_length=100)
    sticker_path = models.CharField(max_length=100, null=True)
    date = models.DateField()
    is_favorite = models.BooleanField(default=False)