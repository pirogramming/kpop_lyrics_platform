import json
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from Kasa.convert_url import convert_youtube
from Kasa.models import Groups, Songs, Singers, Lyrics, Comments


def detail_song(request, song_pk):
    song = get_object_or_404(Songs, pk=song_pk)
    album = song.album
    sns = song.album.group.sns_url
    youtube_url = convert_youtube(song.youtube_url)
    all_lyrics = song.song_lyrics.all()
    comments = song.song_comment.all().order_by('-created_at')

    context = {
        'song': song,
        'album': album,
        'comments': comments,
        'youtube_url': youtube_url,
        'sns': sns,
        'all_lyrics': all_lyrics,
    }
    return render(request, 'Kasa/detail_song.html', context)