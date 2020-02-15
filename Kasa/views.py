import json
import random
import re

import requests
from bs4 import BeautifulSoup
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from Kasa.convert_url import convert_youtube
from Kasa.models import *
from django.db.models import Q

from accounts.decorators import login_required


def song_detail(request, song_pk):
    song = get_object_or_404(Songs, pk=song_pk)
    song.view_count += 1
    song.save()

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
    return render(request, 'Kasa/song_detail.html', context)


def write_new_comment(request):
    if request.method == "POST":
        song = get_object_or_404(Songs, pk=request.POST.get('song_id', None))
        Comments.objects.create(content=request.POST.get('comment_content', ''), user=request.user, song=song)
        return redirect('Kasa:song_detail', song.pk)


def choice_group(request):
    if request.method == "POST":
        group_id = request.POST['id']
        context = {
            'group_id': group_id
        }
        return render(request, 'Kasa', context)
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

    return redirect('Kasa:song_detail', song.pk)


def search(request):
    kwd = request.GET.get('kwd', None)
    if not kwd:
        noresult = True
        context = {
            'kwd': kwd,
            'noresult': noresult,
        }
        return render(request, 'Kasa/search_detail.html', context)

    singers_list = []
    songs_list = []
    lyrics_list = []

    singers = Singers.objects.filter(sname__icontains=kwd)
    songs = Songs.objects.filter(sname__icontains=kwd)
    lyrics = Lyrics.objects.filter(Q(kor__icontains=kwd) | Q(rom__icontains=kwd) | Q(eng__icontains=kwd))
    print(singers, songs, lyrics)
    if len(singers) > 5:
        for singers_count in range(5):
            singers_list.append(singers[singers_count])
    else:
        singers_list = singers

    if len(songs) > 5:
        for songs_count in range(5):
            songs_list.append(songs[songs_count])
    else:
        songs_list = songs

    for overlap_check in lyrics:
        if overlap_check in lyrics_list:
            continue
        if len(lyrics) > 5:
            for lyrics_count in range(5):
                lyrics_list.append(lyrics[overlap_check])
        else:
            lyrics_list.append(lyrics[lyrics_count])

    print(singers_list, songs_list, lyrics_list)

    if len(singers_list) <= 0 and len(songs_list) <= 0 and len(lyrics_list) <= 0:
        print('a')
        noresult = False
        context = {
            'kwd': kwd,
            'noresult': noresult,
        }
        return render(request, 'Kasa/search_detail.html', context)

    context = {
        'kwd': kwd,
        'singers': singers_list,
        'songs': songs_list,
        'lyrics': lyrics_list,
        'kwd': kwd,
    }
    return render(request, 'Kasa/search_detail.html', context)


def singer_detail(request, singer_pk):
    singer = get_object_or_404(Singers, pk=singer_pk)
    context = {
        'singer': singer
    }
    return render(request, 'Kasa/singer_detail.html', context)


def group_detail(request, group_pk):
    group = get_object_or_404(Groups, pk=group_pk)
    singers = group.group_singer.all()
    albums = group.group_album.all()
    context = {
        'group': group,
        'singers': singers,
        'albums': albums,
    }
    return render(request, 'Kasa/group_detail.html', context)


def album_detail(request, album_pk):
    album = get_object_or_404(Albums, pk=album_pk)
    url = 'https://www.genie.co.kr/detail/albumInfo?axnm=81097317'
    response = requests.get(url)
    html = response.text
    print(html)
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find("div", "db-insert")
    # a = str(items)
    # prd_names = re.sub('<.+?>', '', a, 0).strip()
    # print(prd_names)
    context = {
        'album': album,
        'items': items,

        # 'prd_names': prd_names,
    }
    return render(request, 'Kasa/album_detail.html', context)


def select_top_5_songs():
    top_5_songs = []
    view_count_all = []
    song_and_view_count = {}

    songs = Songs.objects.all()
    for song in songs:
        view_count = song.view_count
        song_and_view_count[song.id] = view_count
        view_count_all.append(view_count)
    view_count_all.sort()
    for view_count in view_count_all[:-6:-1]:
        for song_id, value in song_and_view_count.items():
            if value == view_count:
                top_5_songs.append(songs.get(pk=song_id))
                songs = songs.exclude(pk=song_id)
                del song_and_view_count[song_id]
                break

    return top_5_songs


def pick_one_group_by_user(user=None):
    if user.is_authenticated and user.interest:
        user_info = user.interest
        interests = user_info.replace(',', ' ')
        interests = interests.replace('/', ' ')
        interests = interests.split(' ')
        group_list = []
        for interest in interests:
            if not interest:
                continue
            sets = Groups.objects.filter(gname__icontains=interest)
            if not sets:
                groups = Groups.objects.all()
                if groups:
                    return random.choice(groups)
                return None
            for query in sets:
                group_list.append(query)
            return random.choice(group_list)
    else:
        groups = Groups.objects.all()
        if groups:
            return random.choice(groups)
        return None


def main(request):
    five_songs = select_top_5_songs()
    group = pick_one_group_by_user(request.user)
    context = {
        'five_songs': five_songs,
        'group': group
    }
    return render(request, 'Kasa/main.html', context)
