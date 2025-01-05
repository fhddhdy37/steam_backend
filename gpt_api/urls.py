from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('hi/', views.hi, name='hi'),
    path('bye/', views.bye, name='bye'),
]