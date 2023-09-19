from django.urls import path
from . import views

urlpatterns = [
    path('original_feed/', views.original_feed, name='original_feed'),
    path('', views.original_stream, name='original_stream'),
    path('mediapipe_feed/', views.mediapipe_feed, name='mediapipe_feed'),
    path('', views.mediapipe_stream, name='mediapipe_stream'),
]