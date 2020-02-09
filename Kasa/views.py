import json
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from Kasa.convert_url import convert_youtube
from Kasa.models import Groups, Songs, Singers, Lyrics, Comments


def detail_song(request, song_pk):
    song = get_object_or_404(Songs, pk=song_pk)
    sns = song.album.group.sns_url
    youtube_url = convert_youtube(song.youtube_url)
    all_lyrics = song.song_lyrics.all()
    comments = song.song_comment.all().order_by('-created_at')
    context = {
        'song': song,
        'comments': comments,
        'youtube_url': youtube_url,
        'sns': sns,
        'all_lyrics': all_lyrics,
    }
    return render(request, 'Kasa/detail_song.html', context)


def write_new_comment(request):
    if request.method == "POST":
        song = get_object_or_404(Songs, pk=request.POST.get('song_id', None))
        Comments.objects.create(content=request.POST.get('comment_content', ''), user=request.user, song=song)
        return redirect('Kasa:detail_song', song.pk)


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
        song = Songs.objects.get(pk=song_id)
        singers = Singers.objects.filter(singer_song=song_id)
        all_kor = request.POST.get('all_kor', None).split('\r\n')

        all_lang_dict = {}
        length = len(all_kor)

        for index, lyrics in enumerate(all_kor):
            all_lang_dict[str(index + 1)] = {'kor': lyrics}

        eng_request = request.POST.get('all_eng', None)
        if eng_request:
            all_eng = eng_request.split('\r\n')
            for index, lyrics in enumerate(all_eng):
                location = all_lang_dict.get(str(index + 1), None)
                location['eng'] = lyrics

        rom_request = request.POST.get('all_rom', None)
        if rom_request:
            all_rom = rom_request.split('\r\n')
            for index, lyrics in enumerate(all_rom):
                location = all_lang_dict.get(str(index + 1), None)
                location['rom'] = lyrics

        print(all_lang_dict)

        context = {
            'song': song,
            'singers': singers,
            'all_lang_dict': all_lang_dict,
            'length': length,
        }
        return render(request, 'Kasa/modify_and_create_each_lyrics.html', context)
    else:
        return render(request, 'Kasa/enter_all_lyrics.html')


def modify_and_create_each_lyrics(request, song_id):
    if request.method == "POST":
        print(request.POST)
        request_dict = request.POST
        song = Songs.objects.get(pk=song_id)
        singers = song.singer.all()
        all_lyrics = song.song_lyrics.all().order_by('order')
        length = int(request.POST['length'])
        if all_lyrics:
            # DB에 저장된 노래가사들이 있을 경우
            print('있음')
            existing_lyrics_length = len(all_lyrics)
            if existing_lyrics_length > length:
                # 새로 들어온 가사가 기존의 가사의 길이보다 작을 경우 삭제
                start = length
                end = existing_lyrics_length
                for over in range(start, end):
                    all_lyrics[over].delete()
            for input_order in range(0, length):
                str_input_order = str(input_order + 1)
                if input_order < existing_lyrics_length:
                    # 기존 순서의 가사가 있을 경우 변경
                    all_lyrics[input_order].kor = request_dict['kor' + str_input_order]
                    all_lyrics[input_order].order = input_order + 1
                    if request_dict['eng' + str_input_order]:
                        all_lyrics[input_order].eng = request_dict['eng' + str_input_order]
                    if request_dict['rom' + str_input_order]:
                        all_lyrics[input_order].rom = request_dict['rom' + str_input_order]
                    if request_dict.get('part' + str_input_order + '[]', False):
                        partList = request_dict.getlist('part' + str_input_order + '[]')
                        all_lyrics[input_order].singer.clear()
                        for member in singers:
                            if member.sname in partList:
                                all_lyrics[input_order].singer.add(member)
                    all_lyrics[input_order].save()
                else:
                    # 기존 순서에 없는 가사가 있을 경우 추가
                    new_lyrics = Lyrics.objects.create(kor=request_dict['kor' + str_input_order],
                                                       order=input_order + 1, song=song)
                    if request_dict['eng' + str_input_order]:
                        new_lyrics.eng = request_dict['eng' + str_input_order]
                    if request_dict['rom' + str_input_order]:
                        new_lyrics.rom = request_dict['rom' + str_input_order]
                    if request_dict.get('part' + str_input_order + '[]', False):
                        partList = request_dict.getlist('part' + str_input_order + '[]')
                        # all_lyrics[input_order].singer.clear()
                        for member in singers:
                            if member.sname in partList:
                                new_lyrics.singer.add(member)
                    new_lyrics.save()

        else:
            # 노래의 가사가 처음 등록되는 경우
            for input_order in range(0, length):
                str_input_order = str(input_order + 1)
                new_lyrics = Lyrics.objects.create(kor=request_dict['kor' + str_input_order],
                                                   order=input_order + 1, song=song)
                if request_dict['eng' + str_input_order]:
                    new_lyrics.eng = request_dict['eng' + str_input_order]
                if request_dict['rom' + str_input_order]:
                    new_lyrics.rom = request_dict['rom' + str_input_order]
                if request_dict.get('part' + str_input_order + '[]', False):
                    partList = request_dict.getlist('part' + str_input_order + '[]')
                    # all_lyrics[input_order].singer.clear()
                    for member in singers:
                        if member.sname in partList:
                            new_lyrics.singer.add(member)
                new_lyrics.save()

    return redirect('Kasa:detail_song', song.pk)
