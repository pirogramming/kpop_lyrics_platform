from django.conf import settings
from django.db import models

# Create your models here.

class Users(models.Model):
    id = models.CharField(max_length=20)
    pw = models.CharField(max_length=20)
    alias = models.CharField(max_length=20)
    email = models.CharField(max_length=50)
    interest = models.CharField(max_length=50)

class Groups(models.Model):
    gname = models.CharField(max_length=50)
    agency = models.CharField(max_length=50)
    sns_url = models.URLField()

class Albums(models.Model):
    release_date = models.DateTimeField()
    album_art = models.TextField()
    group = models.ForeignKey(Groups, on_delete=models.CASCADE)
    album_image = models.ImageField()

class Singers(models.Model):
    sname = models.CharField()
    image = models.ImageField()
    wiki_url = models.URLField()
    group = models.ManyToManyField(Groups)

class Songs(models.Model):
    youtube_url = models.URLField()
    soundcloud_url = models.URLField()
    dance_url = models.URLField()
    album = models.ForeignKey(Albums, on_delete=models.CASCADE)
    singer = models.ManyToManyField(Singers)

class Comments(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    song = models.ForeignKey(Songs, on_delete=models.CASCADE)

class Fandoms(models.Model):
    fname = models.CharField(max_length=20)
    official_url = models.URLField()
    group = models.OneToOneField(Groups, on_delete=models.CASCADE)

class Lyrics(models.Model):
    kor = models.TextField()
    eng = models.TextField()
    rom = models.TextField()
    fanchant = models.TextField()
    order = models.IntegerField()
    song = models.ForeignKey(Songs, on_delete=models.CASCADE)
    singer = models.ManyToManyField(Singers)

class Explanations(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    image = models.ImageField()
    likes = models.IntegerField()
    lyrics = models.ForeignKey(Lyrics)

