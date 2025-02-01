from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    ## API 엔드포인트 설정
    path('getdiary', views.GetDiary.as_view(), name='get-diary'),
    path('postdiary', views.PostDiary.as_view(), name='post-diary'),
    path('imgtest', views.imgtest, name='imgtest'),
    path('getimage', views.GetImage.as_view(), name='getimage'),
]

# 이미지 파일을 직접 접근하는 URL, 테스트 코드
urlpatterns += static(settings.IMAGE_URL, document_root=settings.IMAGE_DIR)