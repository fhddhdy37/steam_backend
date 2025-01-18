from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import DataList

from . import views

urlpatterns = [
    ## API 엔드포인트 설정정
    path('data/', views.DataList.as_view(), name = 'data-list'),
    path('imgtest/', views.imgtest, name='imgtest'),
]

urlpatterns += static(settings.IMAGE_URL, document_root=settings.IMAGE_DIR)