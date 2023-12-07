from django.urls import path
from . import views

urlpatterns = [
    ## Movies ##
    # GET: 전체 영화 리스트 조회
    path("", views.movie_list, name="movie_list"),
    # GET: 단일 영화 조회
    path("<int:movie_id>/", views.movie_detail, name="movie_detail"),
    ## Reviews ##
    # GET: 전체 리뷰 리스트 조회  # POST: 리뷰 생성
    path("<int:movie_id>/reviews/", views.review_list, name="review_list"),
    # PUT: 리뷰 수정  # DELETE: 리뷰 삭제
    path("reviews/<int:review_pk>/", views.review_detail, name="review_detail"),
    # GET: 추천 영화 조회
    path("recommend/", views.recommend_movies),
    # GET: 숨은 명작 영화 조회
    path("recommend_hidden/", views.recommend_hidden_movies),
    # GET: 추천받은 영화 리스트
    path("list/<int:movie_id>", views.movie_list),
]
