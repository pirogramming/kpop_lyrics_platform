import json
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from Kasa.convert_url import convert_youtube
from Kasa.models import Groups, Songs, Singers


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
    if request.method == "POST":
        group_id = request.POST['id']
        context = {
            'group_id': group_id
        }
        # return render(request, 'Kasa'/)
    else:
        return render(request, 'Kasa/choice_group.html')


def search_group(request):
    kwd = request.POST.get('kwd', None)
    data = {
        'content': list()
    }
    if kwd:
        groups = Groups.objects.filter(gname__icontains=kwd)
        for group in groups:
            data['content'].append({
                'id': group.id,
                'name': group.gname,
            })
    return HttpResponse(json.dumps(data), content_type="application/json")


def enter_all_lyrics(request, song_id):
    if request.method == "POST":
        all_kor = request.POST.get('all_kor', None).split('\r\n')
        all_kor_dict = list()

        song = Songs.objects.get(pk=song_id)
        singers = Singers.objects.filter(singer_song=song_id)
        length = len(all_kor)

        for index, lyrics in enumerate(all_kor):
            all_kor_dict.append({
                str(index + 1): lyrics
            })

        context = {
            'song': song,
            'singers': singers,
            'all_kor_dict': all_kor_dict,
            'length': length,
        }
        return render(request, 'Kasa/modify_each_lyrics.html', context)
    else:
        return render(request, 'Kasa/enter_all_lyrics.html')


def modify_each_lyrics(request, song_id):
    if request.method == "POST":
        song = Songs.objects.get(pk=song_id)
        request_dict = request.POST
        lyrics_all = list()
        length = int(request_dict['length'])
        for index in range(1, length + 1):
            str_index = str(index)
            lyrics_all.append({
                'kor': request_dict['kor' + str_index],
                'eng': request_dict['eng' + str_index],
                'rom': request_dict['rom' + str_index],
            })
            if 'part' + str_index + '[]' in request_dict:
                partList = request_dict.getlist('part' + str_index + '[]')
                # for member in partList:
                lyrics_all[index-1]['part'] = partList
            else:
                lyrics_all[index-1]['part'] = ''

        print(lyrics_all)
        context = {
            'song': song,
            'lyrics_all': lyrics_all,
        }
        return render(request, 'Kasa/double_check_request.html', context)


def create_all_lyrics(request):
    if request.method == "POST":
        print(request.POST)