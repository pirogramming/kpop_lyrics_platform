from django.shortcuts import render, get_object_or_404

from Kasa.convert_url import convert_youtube
from Kasa.models import Groups, Songs


def test(request):
    return render(request, 'Kasa/test.html')

def detail_song(request, song_pk):
    song = get_object_or_404(Songs, pk=song_pk)
    print(song.youtube_url)
    sns = song.album.group.sns_url
    youtube_url = convert_youtube(song.youtube_url)
    context = {
        'youtube_url': youtube_url,
        'sns': sns,
    }
    return render(request, 'Kasa/detail_song.html', context)