from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import DataList

from . import views

urlpatterns = [
    ## API 엔드포인트 설정정
    path('data/', views.DataList.as_view(), name = 'data-list'),
    
    path('', views.index, name='index'),
    path('hi/', views.hi, name='hi'),
    path('bye/', views.bye, name='bye'),
    path('hihi/', views.hihi, name='hihi'),
    path('getkeyword', views.get_keyword, name='get_keyword'),
    path('imgtest/', views.imgtest, name='imgtest'),
    path('diary/', views.diary, name='diary'),
    path('dbtest/', views.dbtest, name='dbtest'),
    path('addtestdata/', views.add_test_data, name='add_test_data'),
    path('deletealldata/', views.delete_all_data, name='delete_all_data'),
    path('getdiarycontent/', views.get_diary_content, name='get_diary_content'),
    path('getdiarycontent2/', views.get_diary_content2, name='get_diary_content2'),
    path('gettodaydiary/', views.get_today_diary, name='get_today_diary'),
    path('reportdiary/', views.report_diary, name='report_diary'),
]

urlpatterns += static(settings.IMAGE_URL, document_root=settings.IMAGE_DIR)