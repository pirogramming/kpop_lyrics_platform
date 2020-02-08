from django.shortcuts import render
from django.db.models import Q

# Create your views here.
from Kasa.models import Songs, Lyrics, Explanations, Singers


def search(request):
    singers = Singers.objects.all()
    songs = Songs.objects.all()
    lyrics = Lyrics.objects.all()

    kwd = request.GET.get('kwd', '')
    if kwd:
        singers = singers.filter(sname__icontains=kwd)
        songs = songs.filter(sname__icontains=kwd)
        lyrics = lyrics.filter(
            Q(kor__icontains=kwd) | Q(eng__icontains=kwd) | Q(rom__icontains=kwd)
        )

    return render(request, 'Kasa/search_detail.html', {
        'singer_list' : singers,
        'song_list' : songs,
        'lyrics_list' : lyrics,
        'kwd':kwd,
    })

    """
    :method: GET
    :param request:
    request.GET['keyword']; 검색 키워드
    :return:
    render_template('search/search_detail.html')

    singer_list = [Singers]; max length 10
    album_list = [Albums]; max length 10
    song_list = [Songs]; max length 10
    lyrics_list = [Lyrics]; max length 10

    """

    raise NotImplementedError


def select_top_5_songs():
    """
    5개의 노래를 뽑아서 리턴하세요.
    :return: a list of songs
    """
    raise NotImplementedError


def pick_one_group_by_user(user=None):
    """
    만약 로그인이면, 관심사 그룹을 보여주고 아니면 랜덤픽
    :return:
    """
    raise NotImplementedError


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
    return render(request, 'main.html', context={
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

    raise NotImplementedError
