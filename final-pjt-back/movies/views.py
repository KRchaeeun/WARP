from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated  # IsAuthenticated 추가
from django.http import JsonResponse


from django.shortcuts import get_object_or_404, get_list_or_404

from .models import Movie, Review, Genre, Video

from .serializers import MovieSerializer, ReviewSerializer, MovieListSerializer

import requests
from requests.exceptions import RequestException
from django.conf import settings

TMDB_ACCESS_TOKEN = settings.TMDB_ACCESS_TOKEN
headers = {"accept": "application/json", "Authorization": f"Bearer {TMDB_ACCESS_TOKEN}"}

# # authentication_classes Decorators
# from rest_framework.decorators import authentication_classes
# from rest_framework.authentication import TokenAuthentication, BasicAuthentication
# # permission Decorators
# from rest_framework.decorators import permission_classes
# from rest_framework.permissions import IsAuthenticated, IsAdminUser


## Movies ##
# GET: 전체 영화 리스트 조회
@api_view(["GET"])
def movie_list(request):
    movies = get_list_or_404(Movie)
    serializer = MovieListSerializer(movies, many=True)
    return Response(serializer.data)


# GET: 단일 영화 조회
@api_view(["GET"])
def movie_detail(request, movie_id):
    try:
        movie = Movie.objects.get(pk=movie_id)
        serializer = MovieSerializer(movie)
        return Response(serializer.data)
    except Movie.DoesNotExist:
        pass  # 해당 ID의 영화가 DB에 없을 때 계속 진행
    except Exception as e:
        print(f"An error occurred: {e}")
        return Response(
            {"error": "An error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    try:
        detail_url = f"https://api.themoviedb.org/3/movie/{movie_id}?language=ko-KR"
        video_url = (
            f"https://api.themoviedb.org/3/movie/{movie_id}/videos?language=ko-KR"
        )

        # requests.get() 예외 처리 추가
        detail_response = requests.get(detail_url, headers=headers)
        detail_response.raise_for_status()
        detail_result = detail_response.json()

        video_response = requests.get(video_url, headers=headers)
        video_response.raise_for_status()
        video_result = video_response.json()
        video_flag = False

        if video_result.get("results"):
            video_flag = True
            video_id = video_result["results"][0]["id"]
            video = Video(
                id=video_id,
                name=video_result["results"][0]["name"],
                key=video_result["results"][0]["key"],
                video_type=video_result["results"][0]["type"],
            )

            video.save()

        # 영화 DB 저장
        movie = Movie(
            id=movie_id,
            title=detail_result["title"],
            overview=detail_result["overview"],
            release_date=detail_result["release_date"],
            runtime=str(detail_result["runtime"]),  # runtime을 문자열로 저장
            poster_path=detail_result["poster_path"],
            popularity=detail_result["popularity"],
            vote_average=detail_result["vote_average"],
        )
        movie.save()
        if video_flag:
            movie.videos.set([video])
        serializer = MovieSerializer(movie)

        return Response(serializer.data)
    except RequestException as e:
        print(f"Request error: {e}")
        return Response(
            {"error": "Error in API request"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return Response(
            {"error": "An unexpected error occurred"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


## Reviews ##
# GET: 전체 리뷰 리스트 조회  # POST: 리뷰 생성
@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])  # IsAuthenticated 데코레이터 사용
def review_list(request, movie_id):
    # GET: 전체 리뷰 리스트 조회
    if request.method == "GET":
        reviews = Review.objects.filter(movie_id=movie_id)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    # POST: 리뷰 생성
    elif request.method == "POST":
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            movie = get_object_or_404(Movie, pk=movie_id)  # movie 객체 가져오기

            # 로그인한 사용자를 얻어옵니다.
            user = request.user

            # 리뷰 모델을 저장하기 전에 user를 할당합니다.
            serializer.save(movie=movie, user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# PUT: 리뷰 수정  # DELETE: 리뷰 삭제
@api_view(["PUT", "DELETE"])
def review_detail(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)

    # PUT: 리뷰 수정
    if request.method == "PUT":
        serializer = ReviewSerializer(review, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE: 리뷰 삭제
    elif request.method == "DELETE":
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# from django.db.models.expressions import RawSQL
from django.db.models import Avg
from datetime import date
import numpy as np


# def recommend_movies(request):
#     year = request.GET.get("year", date.today().year)  # 기본값은 현재 년도
#     genre = request.GET.get("genre", None)

#     # vote_average 필드의 75% 백분위수 값 구하기
#     # percentile_75 = (
#     #     Movie.objects.annotate(
#     #         percentile_75=RawSQL(
#     #             "PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY %s)", ["popularity"]
#     #         )
#     #     )
#     #     .first()
#     #     .percentile_75
#     # )

#     # popularity 값을 리스트로 추출
#     popularity_values = list(Movie.objects.values_list("popularity", flat=True))
#     # numpy를 사용하여 75% 백분위수 계산
#     percentile_75 = np.percentile(popularity_values, 75)

#     print(percentile_75)

#     # popularity 필드 평균값 구하기
#     average_vote = Movie.objects.aggregate(Avg("vote_average"))["vote_average__avg"]

#     print(average_vote)

#     query = Movie.objects.filter(
#         release_date__year=year,
#         popularity__lte=percentile_75,
#         vote_average__gte=average_vote,
#     )

#     if genre:
#         query = query.filter(genres__name=genre)

#     recommended_movies = query

#     serializer = MovieListSerializer(recommended_movies, many=True)
#     return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
def recommend_hidden_movies(request):
    # 연도 리스트 받기 (기본값은 모든 연도)
    years = request.GET.getlist("year")  # 여러 연도를 리스트로 받음
    if not years:
        years = Movie.objects.dates("release_date", "year").values_list(
            "release_date__year", flat=True
        )

    expanded_years = []
    for year in years:
        if year.endswith("s"):
            for i in range(0, 10):
                expanded_years.append(f"{year[:-2]}{i}")
        else:
            expanded_years.append(year)
    # 장르 리스트 받기 (기본값은 모든 장르)
    genres = request.GET.getlist("genre")  # 여러 장르를 리스트로 받음
    print(expanded_years)
    if not genres:
        genres = Genre.objects.values_list("name", flat=True)

    # popularity 값을 리스트로 추출
    popularity_values = list(Movie.objects.values_list("popularity", flat=True))

    # numpy를 사용하여 50% 백분위수 계산
    percentile_50 = np.percentile(popularity_values, 50)
    # popularity 필드 평균값 구하기
    average_vote = Movie.objects.aggregate(Avg("vote_average"))["vote_average__avg"]

    # 기본 쿼리 설정
    query = Movie.objects.filter(
        release_date__year__in=expanded_years,  # 연도 필터
        popularity__lte=percentile_50,
        vote_average__gte=average_vote,
    ).order_by("-vote_average")

    # 장르 필터 적용
    if genres:
        query = query.filter(genres__name__in=genres).distinct()

    recommended_movies = query[:10]

    serializer = MovieListSerializer(recommended_movies, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
    # return Response(status=status.HTTP_200_OK)
    # return JsonResponse(serializer.data, status=200)


@api_view(["GET"])
def recommend_movies(request):
    # 연도 리스트 받기 (기본값은 모든 연도)
    years = request.GET.getlist("year")  # 여러 연도를 리스트로 받음
    if not years:
        years = Movie.objects.dates("release_date", "year").values_list(
            "release_date__year", flat=True
        )

    expanded_years = []
    for year in years:
        if year.endswith("s"):
            for i in range(0, 10):
                expanded_years.append(f"{year[:-2]}{i}")
        else:
            expanded_years.append(year)
    # 장르 리스트 받기 (기본값은 모든 장르)
    genres = request.GET.getlist("genre")  # 여러 장르를 리스트로 받음

    if not genres:
        genres = Genre.objects.values_list("name", flat=True)

    average_vote = Movie.objects.aggregate(Avg("vote_average"))["vote_average__avg"]

    # 기본 쿼리 설정
    query = Movie.objects.filter(
        release_date__year__in=expanded_years,  # 연도 필터
        vote_average__gte=average_vote,
    ).order_by("-popularity")

    # 장르 필터 적용
    if genres:
        query = query.filter(genres__name__in=genres).distinct()

    recommended_movies = query[:10]

    serializer = MovieListSerializer(recommended_movies, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# GET : 추천받은 영화 조회
@api_view(["GET"])
def movie_list(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    serializer = MovieSerializer(movie)
    return Response(serializer.data)
