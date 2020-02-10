from django.urls import path

app_name = 'Kasa'

urlpatterns = [
    path('detail_song/<int:song_pk>/', views.detail_song, name='detail_song'),
    path('', views.main, name='main'),
    path('search/', views.search, name='search'),
    path('singer/<int:pk>', views.singer_detail, name='singer_detail'),
    path('group/<int:pk>', views.group_detail, name='group_detail'),
    path('album/<int:pk>', views.album_detail, name='album_detail'),
    path('song/<int:pk>', views.song_detail, name='song_detail'),
]
