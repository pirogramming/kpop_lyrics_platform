from django.shortcuts import render, get_object_or_404
from django.db.models import Q

# Create your views here.
from Kasa.models import *
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

def search(request):
    kwd = request.GET.get('kwd', '')

    singers_list = []
    songs_list =[]
    lyrics_list = []

    singers = Singers.objects.filter(sname__icontains=kwd)
    songs = Songs.objects.filter(sname__icontains=kwd)
    lyrics = Lyrics.objects.filter(Q(kor__icontains=kwd) | Q(rom__icontains=kwd) | Q(eng__icontains=kwd))

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

    if len(lyrics) > 5:
        for lyrics_count in range(5):
            lyrics_list.append(lyrics[lyrics_count])
    else:
        lyrics_list = lyrics
    return render(request, 'Kasa/search_detail.html', {
        'singers': singers_list,
        'songs': songs_list,
        'lyrics': lyrics_list,
        'kwd': kwd,
    })

def singer_detail(request, pk):
    singer = get_object_or_404(Singers, pk=pk)
    return render(request, 'Kasa/singer_detail.html', {
        'singer' : singer
    })

def group_detail(request, pk):
    group = get_object_or_404(Groups, pk=pk)
    return render(request, 'Kasa/group_detail.html', {
        'group' : group
    })

def album_detail(request, pk):
    album = get_object_or_404(Albums, pk=pk)
    return render(request, 'Kasa/album_detail.html', {
        'album' : album
    })

def song_detail(request, pk):
    song = get_object_or_404(Songs, pk=pk)
    return render(request, 'Kasa/song_detail.html', {
        'song' : song
    })

def select_top_5_songs():
    """
    5개의 노래를 뽑아서 리턴하세요.
    :return: a list of songs
    """
    # raise NotImplementedError


def pick_one_group_by_user(user=None):
    """
    만약 로그인이면, 관심사 그룹을 보여주고 아니면 랜덤픽
    :return:
    """
    # raise NotImplementedError


def main(request):
    """
    method: GET
    :param request:
    :return:
    render_template('main.html')

    five_songs = [Songs]; length 5
    group = Group  # group.singers

    """
    five_songs = select_top_5_songs()
    group = pick_one_group_by_user(request.user)
    return render(request, 'main_revised_second_version.html', context={
        'five_songs': five_songs,
        'group': group
    })


def show_lyric(request):
    """
    method : GET

    :param request:
    request.GET.song_id;

    :return:

    render_template('explanation.html')

    explanation : Explanations

    """
    song = Songs.objects.get(id=request.GET.song_id)
    lyrics = Lyrics.objects.filter(song_id=song.id)
    explanations = list()
    for lyric in lyrics:
        explanations += Explanations.objects.filter(lyrics_id=lyric.id)

    max_explanation = None
    max_likes = -1
    for explanation in explanations:
        if explanation.likes > max_likes:
            max_explanation = explanation

    # raise NotImplementedError
