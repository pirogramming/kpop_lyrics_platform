from django.urls import path

app_name = 'Kasa'

urlpatterns = [
    path('detail_song/<int:song_pk>/', views.detail_song, name='detail_song'),
    path('comment/new/', views.write_new_comment, name='write_new_comment'),
    path('edit/<int:song_id>/stage1/', views.enter_all_lyrics, name='enter_all_lyrics'),
    path('edit/<int:song_id>/stage2/', views.modify_and_create_each_lyrics, name='modify_and_create_each_lyrics'),






    path('choice_group/', views.choice_group, name='choice_group'),
    path('search_group/', views.search_group, name='search_group'),
    path('', views.main, name='main'),
    path('search/', views.search, name='search'),
    path('singer/<int:pk>', views.singer_detail, name='singer_detail'),
    path('group/<int:pk>', views.group_detail, name='group_detail'),
    path('album/<int:pk>', views.album_detail, name='album_detail'),
]
