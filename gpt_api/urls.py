from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('hi/', views.hi, name='hi'),
    path('bye/', views.bye, name='bye'),
    path('hihi/', views.hihi, name='hihi'),
    # path('getkeyword', views.get_keyword, name='get_keyword'),
    path('imgtest/', views.imgtest, name='imgtest'),
    
]

urlpatterns += static(settings.IMAGE_URL, document_root=settings.IMAGE_DIR)