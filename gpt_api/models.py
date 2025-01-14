from django.db import models

# Create your models here.

class User(models.Model):
    nickname = models.CharField(max_length=15)
    id = models.CharField(max_length=20, primary_key=True)
    password = models.CharField(max_length=20)

class Diary(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()
    date = models.DateField()
    sticker_path = models.CharField(max_length=100, null=True)