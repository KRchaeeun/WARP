from django.db import models

# settings.AUTH_USER_MODEL 사용을 위한 import
from django.conf import settings


## Genre 모델 ##


# Issue: 장르를 따로 빼는 이유 확인 필요
# -> 받아오는 데이터 형태 확인
class Genre(models.Model):
    # 장르 종류
    # id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)


class Actor(models.Model):  # 배우 DB
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    popularity = models.FloatField()  # 배우 인기도
    profile_path = models.TextField(null=True, blank=True)  # 프로필사진 이미지 주소


class Director(models.Model):  # 감독 DB
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    popularity = models.FloatField()  # 감독 인기도
    profile_path = models.TextField(null=True, blank=True)  # 프로필사진 이미지 주소


class Provider(models.Model):  # 공급 DB
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    logo_path = models.CharField(max_length=100)
    display_priority = models.IntegerField()


class Keyword(models.Model):  # 키워드 DB
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)


## Video 모델 ##
# lee: Video 모델 추가
# models.py
class Video(models.Model):
    # movie = models.ForeignKey(Movie, related_name="videos", on_delete=models.CASCADE)
    id = models.CharField(primary_key=True, max_length=100)
    name = models.CharField(max_length=50)
    key = models.CharField(max_length=50)
    video_type = models.CharField(max_length=50)


## Movie 모델 ##


class Movie(models.Model):
    id = models.IntegerField(primary_key=True)
    # 영화 제목
    title = models.CharField(max_length=100)

    # 영화 개요
    overview = models.TextField()
    # 영화 개봉일
    release_date = models.DateField()
    # 영화 상영 시간
    # Issue: runtime을 integerField 또는 TextField로 할지 확인 필요
    # -> 영화 상영 시간 순으로 데이터를 가공할 필요가 없기 때문에 TextField로 설정
    runtime = models.TextField()
    # 영화 포스터 경로
    poster_path = models.CharField(max_length=200)
    # 배경 이미지 주소
    backdrop_path = models.TextField()
    # 영화 티저 영상
    video = models.ManyToManyField("Video", blank=True, related_name="movies")
    # 영화 인기도
    popularity = models.FloatField()  # lee: 알고리즘에 사용할 인기도 추가
    # 영화 평균 평점
    vote_average = models.FloatField()  # lee: 알고리즘에 사용할 평균 별점 추가
    # 상태
    status = models.CharField(max_length=50, null=True, blank=True)
    # 슬로건
    tagline = models.TextField(null=True, blank=True)

    # 다대다 모델 -> 중개모델 생성
    # 영화 장르
    genres = models.ManyToManyField(Genre)
    actors = models.ManyToManyField(Actor, blank=True)
    directors = models.ManyToManyField(Director, blank=True)
    keywords = models.ManyToManyField(Keyword, blank=True)
    videos = models.ManyToManyField(Video, blank=True)


## Review 모델 ##


class Review(models.Model):
    # 리뷰 할 영화
    movie = models.ForeignKey(
        Movie, on_delete=models.CASCADE, related_name="movie_reviews"
    )
    # 리뷰 작성자
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_reviews"
    )
    # # 리뷰 제목
    # title = models.CharField(max_length=100)
    # 리뷰 내용
    content = models.TextField()
    # 리뷰 점수
    # Issue. ERD를 real말고 float로 변경 필요
    # django 모델 필드 중에 실수의 경우 real이 아닌 float로 표현
    rating = models.FloatField()
    # 리뷰 생성 일시
    # auto_now_add=True : 레코드가 생성될 때 자동으로 현재 일시로 설정
    created_at = models.DateTimeField(auto_now_add=True)
