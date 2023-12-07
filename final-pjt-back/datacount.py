import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "movie_pjt.settings")
django.setup()

from django.db.models import Count, F, Func
from django.db.models.functions import ExtractYear
from movies.models import Movie

# 모든 영화의 제목과 출시일을 출력
# for movie in Movie.objects.all():
#     print(
#         f"Title: {movie.title}, Release Date: {movie.release_date} ({type(movie.release_date)})"
#     )


# 년도별로 영화 개수 집계
movies_per_year = (
    Movie.objects.annotate(year=ExtractYear("release_date"))
    .values("year")
    .annotate(count=Count("id"))
    .order_by("year")
)

for entry in movies_per_year:
    print(f"Year: {entry['year']}, Count: {entry['count']}")

# 년도별로 영화 개수 집계
# 10년 단위로 끊어서 영화 개수 집계
movies_per_decade = (
    Movie.objects.annotate(decade=ExtractYear("release_date") / 10 * 10)
    .values("decade")
    .annotate(count=Count("id"))
    .order_by("decade")
)

for entry in movies_per_decade:
    print(f"Decade: {int(entry['decade'])}s, Count: {entry['count']}")

import json
from movies.models import Movie, Genre, Video

# # Movie 모델의 인스턴스를 JSON으로 변환
# movies = list(Movie.objects.all().values())
# for movie in movies:
#     if "release_date" in movie and movie["release_date"]:
#         movie["release_date"] = movie["release_date"].isoformat()

# with open("movies.json", "w", encoding="utf-8") as file:
#     json.dump(movies, file, ensure_ascii=False, indent=4)

# video 모델의 인스턴스를 JSON으로 변환
# videos = list(Video.objects.all().values())

# with open("videos.json", "w", encoding="utf-8") as file:
#     json.dump(videos, file, ensure_ascii=False, indent=4)

import json
from movies.models import Movie, Genre

# Movie 인스턴스를 JSON으로 변환
movies_data = []
for movie in Movie.objects.all():
    genres = list(movie.genres.values_list("name", flat=True))
    movies_data.append(
        {
            "id": movie.id,
            "title": movie.title,
            "overview": movie.overview,
            "release_date": str(movie.release_date),  # date 객체는 문자열로 변환
            "runtime": movie.runtime,
            "poster_path": movie.poster_path,
            "popularity": movie.popularity,
            "vote_average": movie.vote_average,
            "genres": genres,
        }
    )

# JSON 파일로 저장
with open("movies.json", "w", encoding="utf-8") as file:
    json.dump(movies_data, file, ensure_ascii=False, indent=4)

# Genre 인스턴스를 JSON으로 변환
genres_data = list(Genre.objects.all().values())
# JSON 파일로 저장
with open("genres.json", "w", encoding="utf-8") as file:
    json.dump(genres_data, file, ensure_ascii=False, indent=4)
