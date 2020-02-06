from django.urls import path
from Kasa import views

urlpatterns = [
    path('test/', views.test),
    path('detail_song/<int:song_pk>/', views.detail_song, name='detail_song'),
]