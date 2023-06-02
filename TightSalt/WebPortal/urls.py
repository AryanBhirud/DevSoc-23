from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('team/', views.team, name='team'),
    path('run_face_recog/', views.run_face_recog_page, name='run_face_recog_page'),
    path('result/', views.result_view, name='result'),
    path('register/', views.register, name='register'),
    path('register_new_user', views.register_new_user, name='register_new_user'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
