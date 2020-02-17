import json
import random
import requests
from bs4 import BeautifulSoup
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from Kasa.convert_url import convert_youtube
from Kasa.models import *
from django.db.models import Q
from django.core.paginator import Paginator


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
        request_dict = request.POST
        song = Songs.objects.get(pk=song_id)
        singers = song.singer.all()
        all_lyrics = song.song_lyrics.all().order_by('order')
        length = int(request.POST['length'])
        if all_lyrics:
            # DB에 저장된 노래가사들이 있을 경우
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

    target = request.GET.get('target', '')

    singers_list = []
    songs_list = []
    lyrics_list = []
    albums_list = []
    groups_list = []

    singers = Singers.objects.filter(sname__icontains=kwd)
    songs = Songs.objects.filter(sname__icontains=kwd)
    lyrics = Lyrics.objects.filter(Q(kor__icontains=kwd) | Q(rom__icontains=kwd) | Q(eng__icontains=kwd))
    albums = Albums.objects.filter(aname__icontains=kwd)
    groups = Groups.objects.filter(Q(gname__icontains=kwd) | Q(agency__icontains=kwd))

    if singers:
        for singer in singers:
            singers_list.append(singer)
    if songs:
        for song in songs:
            songs_list.append(song)
    if albums:
        for album in albums:
            albums_list.append(album)
    if groups:
        for group in groups:
            groups_list.append(group)
    if lyrics:
        for overlap_check in lyrics:
            if overlap_check in lyrics_list:
                continue
            lyrics_list.append(overlap_check)

    # 그룹을 검색했을 때 해당 그룹의 앨범,노래,가수
    if groups:
        for group in groups:
            for group_singer in group.group_singer.all():
                singers_list.append(group_singer)
            for group_album in group.group_album.all():
                albums_list.append(group_album)
                for group_song in group_album.album_song.all():
                    songs_list.append(group_song)

    # 가수를 검색했을 때 해당 가수의 그룹,앨범
    if singers:
        for singer in singers:
            for singer_group in singer.group.all():
                groups_list.append(singer_group)
                for singer_album in singer_group.group_album.all():
                    albums_list.append(singer_album)

    # 앨범을 검색했을 때 해당 앨범의 그룹,노래
    if albums:
        for album in albums:
            groups_list.append(album.group)
            for album_song in album.album_song.all():
                songs_list.append(album_song)

    # 노래를 검색했을 때 해당 노래의 앨범과 그룹
    if songs:
        for song in songs:
            if song.album in albums_list:
                pass
            else:
                albums_list.append(song.album)
            if song.album.group in groups_list:
                pass
            else:
                groups_list.append(song.album.group)

    if len(singers_list) <= 0 and len(singers_list) <= 0 and len(groups_list) and len(lyrics_list) <= 0 \
            and len(albums_list) <= 0:
        noresult = True
        context = {
            'kwd': kwd,
            'noresult': noresult,
            'artist_length': 0,
        }
        return render(request, 'Kasa/search_detail.html', context)

    if request.GET.get('is_livesearch', None):
        data = {
            'groups': list(),
            'singers': list(),
            'songs': list(),
        }
        for group_limit_in in groups_list[:2]:
            data['groups'].append({
                'id': group_limit_in.id,
                'name': group_limit_in.gname,
                'image': group_limit_in.group_image.url,
                'agency': group_limit_in.agency,
            })
        for singer_limit_in in singers_list[:4-len(groups_list[:2])]:
            data['singers'].append({
                'id': singer_limit_in.id,
                'name': singer_limit_in.sname,
                'image': singer_limit_in.image.url,
                'group': singer_limit_in.group.first().gname,
            })

        for song_limit_in in songs_list[:4]:
            data['songs'].append({
                'id': song_limit_in.id,
                'name': song_limit_in.sname,
                'image': song_limit_in.album.album_art.url,
                'group': song_limit_in.album.group.gname,
            })

        return HttpResponse(json.dumps(data), content_type="application/json")

    artists_list = groups_list + singers_list

    double_prev_page = None
    double_next_page = None

    # Artist 페이지네이션
    artists_length = len(artists_list)
    artists_paginator = Paginator(artists_list, 6)
    if request.GET.get('target') == 'artist':
        if request.GET.get('artist_page'):
            present_page = int(request.GET.get('artist_page'))
            if present_page - 2 > 1:
                double_prev_page = present_page - 2
            if present_page + 2 < artists_paginator.num_pages:
                double_next_page = present_page + 2
    artist_post = request.GET.get('artist_page', 1)
    artists_posts = artists_paginator.get_page(artist_post)

    # Song 페이지네이션
    songs_length = len(songs_list)
    songs_paginator = Paginator(songs_list, 10)
    if request.GET.get('target') == 'song':
        if request.GET.get('song_page'):
            present_page = int(request.GET.get('song_page'))
            if present_page - 2 > 1:
                double_prev_page = present_page - 2
            if present_page + 2 < songs_paginator.num_pages:
                double_next_page = present_page + 2
    song_post = request.GET.get('song_page', 1)
    songs_posts = songs_paginator.get_page(song_post)

    # Album 페이지네이션
    albums_length = len(albums_list)
    albums_paginator = Paginator(albums_list, 6)
    if request.GET.get('target') == 'album':
        if request.GET.get('album_page'):
            present_page = int(request.GET.get('album_page'))
            if present_page - 2 > 1:
                double_prev_page = present_page - 2
            if present_page + 2 < albums_paginator.num_pages:
                double_next_page = present_page + 2
    album_post = request.GET.get('album_page', 1)
    albums_posts = albums_paginator.get_page(album_post)

    # Lyric 페이지네이션
    lyrics_length = len(lyrics_list)
    lyrics_paginator = Paginator(lyrics_list, 5)
    if request.GET.get('target') == 'lyric':
        if request.GET.get('lyric_page'):
            present_page = int(request.GET.get('lyric_page'))
            if present_page - 2 > 1:
                double_prev_page = present_page - 2
            if present_page + 2 < lyrics_paginator.num_pages:
                double_next_page = present_page + 2
    lyric_post = request.GET.get('lyric_page', 1)
    lyrics_posts = lyrics_paginator.get_page(lyric_post)

    context = {
        'kwd': kwd,
        'artists': artists_posts,
        'songs': songs_posts,
        'albums': albums_posts,
        'lyrics': lyrics_posts,
        'artists_length': artists_length,
        'songs_length': songs_length,
        'albums_length': albums_length,
        'lyrics_length': lyrics_length,
        'double_prev_page': double_prev_page,
        'double_next_page': double_next_page,
        'target': target,
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
        kwd_group_list = []
        choice_group = None
        for interest in interests:
            if not interest:
                continue
            sets = Groups.objects.filter(gname__icontains=interest)
            if not sets:
                continue
            for query in sets:
                kwd_group_list.append(query)
        if kwd_group_list:
            group = random.choice(kwd_group_list)
            while not group.group_image:
                kwd_group_list.remove(group)
                if not kwd_group_list:
                    group = None
                    break
                group = random.choice(kwd_group_list)
            choice_group = group
            if choice_group:
                return choice_group

        group_list = list(Groups.objects.all())
        if not group_list:
            return None

        group = random.choice(group_list)
        while not group.group_image:
            group_list.remove(group)
            if not group_list:
                return None
            group = random.choice(group_list)
        return group

    else:
        groups = Groups.objects.all()
        groups = list(groups)

        if groups:
            group = random.choice(groups)
            while not group.group_image:
                groups.remove(group)
                if not groups:
                    return None
                group = random.choice(groups)
            return group
        return None


def main(request):
    five_songs = select_top_5_songs()
    group = pick_one_group_by_user(request.user)
    context = {
        'five_songs': five_songs,
        'group': group,
    }
    return render(request, 'Kasa/main.html', context)
