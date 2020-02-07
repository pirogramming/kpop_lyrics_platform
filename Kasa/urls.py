from django.urls import path
from Kasa import views

app_name = 'Kasa'

urlpatterns = [
    path('detail_song/<int:song_pk>/', views.detail_song, name='detail_song'),
    path('edit/<int:song_id>/stage1/', views.enter_all_lyrics, name='enter_all_lyrics'),
    path('edit/<int:song_id>/stage2/', views.modify_each_lyrics, name='modify_each_lyrics'),






    path('choice_group/', views.choice_group, name='choice_group'),
    path('search_group/', views.search_group, name='search_group'),
]
