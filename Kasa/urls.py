from django.urls import path
from Kasa import views

app_name = 'Kasa'

urlpatterns = [
    path('', views.main, name='main'),
    path('search/', views.search, name='search'),
    path('song/<int:song_pk>/', views.song_detail, name='song_detail'),
    path('singer/<int:singer_pk>', views.singer_detail, name='singer_detail'),
    path('group/<int:group_pk>', views.group_detail, name='group_detail'),
    path('album/<int:album_pk>', views.album_detail, name='album_detail'),
    path('comment/new/', views.write_new_comment, name='write_new_comment'),
    path('edit/<int:song_id>/stage1/', views.enter_all_lyrics, name='enter_all_lyrics'),
    path('edit/<int:song_id>/stage2/', views.modify_and_create_each_lyrics, name='modify_and_create_each_lyrics'),
    path('choice_group/', views.choice_group, name='choice_group'),
    path('search_group/', views.search_group, name='search_group'),
]