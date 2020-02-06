import json

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from Kasa.convert_url import convert_youtube
from Kasa.models import Groups, Songs


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


def choice_group(request):
    if request.GET:
        pass
    else:
        return render(request, 'Kasa/choice_group.html')


def search_group(request):
    kwd = request.POST.get('kwd', None)
    print(request.POST)
    print(kwd)
    groups = Groups.objects.filter(gname__icontains=kwd)
    print(groups)
    data = {
        # 'count': len(groups),
        'content': ''
    }
    # if data['count'] > 0:
    for group in groups:
        data['content'] = group.gname
        # data['content'].append({
        #     'name': group.gname
        # })
    # print(data['count'])
    return HttpResponse(json.dumps(data), content_type="application/json")


def enter_all_lyrics(request):
    if request.method == "POST":
        all_kor = request.POST.get('all_kor').split('\r\n')
        all_eng = request.POST.get('all_eng').split('\r\n')
        all_rom = request.POST.get('all_rom').split('\r\n')
        print(all_kor, all_eng, all_rom)
    else:
        return render(request, 'Kasa/enter_all_lyrics.html')


def split_lyrics(request):
    pass
