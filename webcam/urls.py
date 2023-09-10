from django.urls import path
from . import views

urlpatterns = [
    path('video/', views.webcam_video_feed, name='webcam_video_feed'),
    path('', views.webcam_video_stream, name='webcam_video_stream'),
]
