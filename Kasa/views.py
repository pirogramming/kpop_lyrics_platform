from django.shortcuts import render

# Create your views here.


def search_live(request):
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

