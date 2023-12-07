import requests
import json

# from django.http import JsonResponse


# # API 키
# from django.conf import settings
# from dotenv import load_dotenv
import django
import os

# # .env 파일의 경로 지정
# dotenv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
# # .env 파일 로드
# load_dotenv(dotenv_path)

# # TMDB API 키 가져오기
# TMDB_API_KEY = os.getenv('VITE_TMDB_API_KEY')
# TMDB_ACCESS_TOKEN = os.getenv('TMDB_ACCESS_TOKEN')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "movie_pjt.settings")
django.setup()

from django.conf import settings
from movies.models import Genre, Movie, Video

# TMDB_API_KEY = settings.TMDB_API_KEY
TMDB_ACCESS_TOKEN = settings.TMDB_ACCESS_TOKEN

# TMDB_API_KEY를 확인
print(f"Using TMDB API Key: {TMDB_ACCESS_TOKEN}")


## 장르 ##

url = "https://api.themoviedb.org/3/genre/movie/list?language=ko"

headers = {"accept": "application/json", "Authorization": f"Bearer {TMDB_ACCESS_TOKEN}"}

response = requests.get(url, headers=headers)
if response.status_code == 200:
    genres_data = response.json().get("genres", [])

    # genres_data를 기반으로 Genre 모델 객체 생성 및 저장
    for genre_data in genres_data:
        # print(genres_data)
        genre, created = Genre.objects.get_or_create(
            id=genre_data["id"], name=genre_data["name"]
        )
        print(
            f"Genre '{genre.name}' {'created' if created else 'already exists'} in the database."
        )
else:
    print("Failed to fetch genre data from TMDB:", response.status_code)


## 영화, 비디오 목록 ##

TMDB_API_URL = "https://api.themoviedb.org/3/movie/top_rated"

for i in range(1, 500):
    print(i)
    params = {
        "language": "ko-KR",
        "page": i,
    }

    response = requests.get(TMDB_API_URL, params=params, headers=headers)

    if response.status_code == 200:
        movies = response.json().get("results", [])
        # NULL 값을 가진 필드를 제외하고 반환
        result = [movie for movie in movies if None not in movie.values()]
    else:
        result = []

    for movie_data in result:
        movie_id = movie_data["id"]
        genre_id = movie_data["genre_ids"]
        detail_url = f"https://api.themoviedb.org/3/movie/{movie_id}?language=ko-KR"
        video_url = (
            f"https://api.themoviedb.org/3/movie/{movie_id}/videos?language=ko-KR"
        )
        detail_response = requests.get(detail_url, headers=headers)
        detail_result = detail_response.json()
        video_response = requests.get(video_url, headers=headers)
        video_result = video_response.json()
        if video_result["results"] == []:
            continue
        # print(genre_id)

        # 영화 DB 저장
        movie = Movie(
            id=movie_id,
            title=movie_data["title"],
            overview=movie_data["overview"],
            release_date=movie_data["release_date"],
            runtime=str(detail_result["runtime"]),  # runtime을 문자열로 저장
            poster_path=movie_data["poster_path"],
            popularity=movie_data["popularity"],
            vote_average=movie_data["vote_average"],
        )
        movie.save()

        # 장르 인스턴스 찾기
        genre_instances = Genre.objects.filter(id__in=genre_id)
        # 장르 연결
        movie.genres.set(genre_instances)

        # 비디오 DB 저장
        video = Video(
            id=movie_id,
            name=video_result["results"][0]["name"],
            key=video_result["results"][0]["key"],
            video_type=video_result["results"][0]["type"],
        )
        video.save()
