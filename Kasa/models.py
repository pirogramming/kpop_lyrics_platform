from django.db import models
from accounts.models import User


class Groups(models.Model):
    gname = models.CharField(max_length=255, verbose_name='그룹이름')
    agency = models.CharField(max_length=255, blank=True, verbose_name='소속사')
    sns_url = models.URLField(verbose_name='SNS', blank=True)
    group_image = models.ImageField(upload_to='group_image', blank=True, verbose_name='그룹사진')
    debut = models.DateField(verbose_name='데뷔일')

    def __str__(self):
        return self.gname


class Albums(models.Model):
    aname = models.CharField(max_length=255, verbose_name='앨범이름')
    release_date = models.DateField(verbose_name='발매일')
    album_art = models.ImageField(upload_to="album_art", verbose_name='자켓사진')
    content = models.TextField(blank=True, verbose_name='앨범소개')
    group = models.ForeignKey(Groups, on_delete=models.CASCADE, verbose_name='그룹이름', related_name='group_album')

    def __str__(self):
        return self.aname


class Singers(models.Model):
    sname = models.CharField(max_length=255, verbose_name='가수이름')
    birth = models.DateField(blank=True, verbose_name='생일')
    image = models.ImageField(upload_to='singer_image', blank=True, verbose_name='가수사진')
    wiki_url = models.URLField(blank=True, verbose_name='가수정보')
    group = models.ManyToManyField(Groups, verbose_name='소속그룹', related_name='group_singer')
    def __str__(self):
        return self.sname


class Songs(models.Model):
    sname = models.CharField(max_length=255, verbose_name='노래제목')
    youtube_url = models.URLField(blank=True, verbose_name='뮤직비디오')
    soundcloud_url = models.URLField(blank=True, verbose_name='오디오')
    dance_url = models.URLField(blank=True, verbose_name='무대영상')
    album = models.ForeignKey(Albums, on_delete=models.CASCADE, verbose_name='앨범', related_name='album_song')
    singer = models.ManyToManyField(Singers, verbose_name='가수', related_name='singer_song')
    view_count = models.IntegerField(default=0, verbose_name='조회수')

    def __str__(self):
        return self.sname


class Comments(models.Model):
    content = models.TextField(verbose_name='내용')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='작성일')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='작성자', related_name='user_comment')
    song = models.ForeignKey(Songs, on_delete=models.CASCADE, verbose_name='노래', related_name='song_comment')

    def __str__(self):
        return self.content

class Lyrics(models.Model):
    kor = models.TextField(verbose_name='한국어')
    eng = models.TextField(blank=True, verbose_name='영어')
    rom = models.TextField(blank=True, verbose_name='로마자')
    fanchant = models.TextField(blank=True, verbose_name='응원법')
    order = models.IntegerField(verbose_name='순서')
    song = models.ForeignKey(Songs, on_delete=models.CASCADE, verbose_name='노래', related_name='song_lyrics')
    singer = models.ManyToManyField(Singers, blank=True, verbose_name='파트', related_name='singer_lyrics')

    def __str__(self):
        return self.song.sname + str(self.order)


class Explanations(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='작성일')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정일')
    content = models.TextField(verbose_name='내용')
    image = models.ImageField(upload_to='explanation_image', blank=True, verbose_name='사진')
    likes = models.IntegerField(default=0, editable=False, verbose_name='좋아요')
    lyrics = models.ForeignKey(Lyrics, on_delete=models.CASCADE, verbose_name='가사', related_name='lyrics_explanation')

    def __str__(self):
        return self.content
