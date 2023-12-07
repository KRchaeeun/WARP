import requests
import json
import os
import django

# Django 설정 및 초기화
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "movie_pjt.settings")
django.setup()

# from movies.models import Genre, Movie, Video

# TMDB API 키 설정
TMDB_API_KEY = os.getenv("TMDB_API_KEY")

# API 요청 URL 설정
TMDB_API_URL = "https://api.themoviedb.org/3/movie/top_rated"
GENRE_API_URL = (
    "https://api.themoviedb.org/3/genre/movie/list?language=ko-KR&api_key="
    + TMDB_API_KEY
)

# JSON 파일 데이터
db_genres_providers_videos = []
db_actors_directors_keywords = []
db_movies = []

# 장르 데이터 가져오기
response = requests.get(GENRE_API_URL)
if response.status_code == 200:
    genres_data = response.json().get("genres", [])
    for genre in genres_data:
        genre_data = {
            "model": "movies.genre",
            "pk": genre["id"],
            "fields": {"name": genre["name"]},
        }
        db_genres_providers_videos.append(genre_data)
# print("장르완료")

# 공급자 데이터 가져오기
# providers_url = (
#     "https://api.themoviedb.org/3/watch/providers/movie?language=ko-KR&watch_region=KR&api_key="
#     + TMDB_API_KEY
# )

# providers = requests.get(providers_url).json()
# for provider in providers["results"]:
#     provider_data = {
#         "model": "movies.provider",
#         "pk": provider["provider_id"],
#         "fields": {
#             "name": provider["provider_name"],
#             "logo_path": provider["logo_path"],
#             "display_priority": provider["display_priority"],
#         },
#     }
#     db_genres_providers_videos.append(provider_data)

# 영화 및 비디오 데이터 가져오기
for page in range(1, 500):
    response = requests.get(
        f"{TMDB_API_URL}?page={page}&language=ko-KR&api_key={TMDB_API_KEY}"
    )
    if response.status_code == 200:
        movies_data = response.json().get("results", [])
        for movie in movies_data:
            movie_detail_url = f"https://api.themoviedb.org/3/movie/{movie['id']}?language=ko-KR&api_key={TMDB_API_KEY}"
            detail_response = requests.get(movie_detail_url)
            if detail_response.status_code == 200:
                detail_data = detail_response.json()

                # 해당 영화의 id값 지정
                movie_id = movie["id"]

                # 디테일 - genre, runtime, status, tagline
                movie_details_url = (
                    "https://api.themoviedb.org/3/movie/"
                    + str(movie_id)
                    + "?language=ko-KR&region=KR&api_key="
                    + TMDB_API_KEY
                )
                movie_details = requests.get(movie_details_url).json()

                # 장르
                genres = []
                for genre in movie_details["genres"]:
                    genres.append(genre["id"])
                if genres == []:
                    continue

                # 런타임
                runtime = movie_details["runtime"]
                if genres == 0:
                    continue

                # 상태
                status = movie_details["status"]
                if status == 0:
                    continue

                # 슬로건
                tagline = movie_details["tagline"]
                if tagline == 0:
                    continue

                # 크레딧
                movie_credits_url = (
                    "https://api.themoviedb.org/3/movie/"
                    + str(movie_id)
                    + "/credits?language=ko-KR&region=KR&api_key="
                    + TMDB_API_KEY
                )
                movie_credit = requests.get(movie_credits_url).json()

                # 정보 누락의 경우 필터링 진행
                credit_flag = True

                # 배우
                actors = []
                actor_datas = []

                for actor in movie_credit["cast"][:5]:
                    actor_id = actor["id"]
                    actors.append(actor_id)

                    actor_name = actor["name"]
                    actor_popularity = actor["popularity"]
                    actor_profile_path = actor["profile_path"]

                    if (
                        actor_name == ""
                        or actor_popularity == 0
                        or actor_profile_path == None
                    ):  # 필터링
                        credit_flag = False
                        break

                    # 배우 DB
                    actor_data = {
                        "model": "movies.actor",
                        "pk": actor_id,
                        "fields": {
                            "name": actor_name,
                            "popularity": actor_popularity,
                            "profile_path": actor_profile_path,
                        },
                    }
                    actor_datas.append(actor_data)

                if not credit_flag or actors == []:
                    continue
                else:
                    db_actors_directors_keywords.extend(actor_datas)
                print("배우완료")

                # 감독
                directors = []
                director_datas = []

                for crew in movie_credit["crew"]:
                    if crew["job"] == "Director":
                        director_id = crew["id"]
                        directors.append(director_id)

                        director_name = crew["name"]
                        director_popularity = crew["popularity"]
                        director_profile_path = crew["profile_path"]

                        if (
                            director_name == ""
                            or director_popularity == 0
                            or director_profile_path == None
                        ):  # 필터링
                            credit_flag = False
                            break

                        # 감독 DB
                        director_data = {
                            "model": "movies.director",
                            "pk": director_id,
                            "fields": {
                                "name": director_name,
                                "popularity": director_popularity,
                                "profile_path": director_profile_path,
                            },
                        }
                        director_datas.append(director_data)

                if not credit_flag or directors == []:
                    continue
                else:
                    db_actors_directors_keywords.extend(director_datas)

                # 키워드 - id, name
                movie_keywords_url = (
                    "https://api.themoviedb.org/3/movie/"
                    + str(movie_id)
                    + "/keywords?language=ko-KR&region=KR&api_key="
                    + TMDB_API_KEY
                )
                movie_keyword = requests.get(movie_keywords_url).json()

                if movie_keyword["keywords"] == []:  # 키워드 없는 영화 필터링
                    continue
                else:
                    keywords = []
                    for keyword in movie_keyword["keywords"]:
                        keyword_id = keyword["id"]
                        keywords.append(keyword_id)

                        keyword_name = keyword["name"]

                        keyword_data = {
                            "model": "movies.keyword",
                            "pk": keyword_id,
                            "fields": {"name": keyword_name},
                        }
                        db_actors_directors_keywords.append(keyword_data)

            # 비디오
            movie_videos_url = (
                "https://api.themoviedb.org/3/movie/"
                + str(movie_id)
                + "/videos?language=ko-KR&region=KR&api_key="
                + TMDB_API_KEY
            )
            movie_videos = requests.get(movie_videos_url).json()

            if movie_videos["results"] == []:
                continue
            else:
                videos = []
                for video in movie_videos["results"]:
                    video_id = video["id"]
                    video_name = video["name"]
                    video_key = video["key"]
                    video_type = video["type"]

                    if (
                        video_id == ""
                        or video_name == ""
                        or video_key == ""
                        or video_type == ""
                    ):
                        continue
                    else:
                        videos.append(video_id)
                        video_data = {
                            "model": "movies.video",
                            "pk": video["id"],
                            "fields": {
                                "name": video["name"],
                                "key": video["key"],
                                "video_type": video["type"],
                            },
                        }
                        db_genres_providers_videos.append(video_data)

                # 영화 데이터 저장
            movie_data = {
                "model": "movies.movie",
                "pk": movie["id"],
                "fields": {
                    "title": movie["title"],
                    "overview": movie["overview"],
                    "release_date": movie["release_date"],
                    "popularity": movie["popularity"],
                    "vote_average": movie["vote_average"],
                    "poster_path": movie["poster_path"],
                    "backdrop_path": movie["backdrop_path"],
                    "runtime": runtime,
                    "status": status,
                    "tagline": tagline,
                    "genres": genres,
                    "actors": actors,
                    "directors": directors,
                    "keywords": keywords,
                    "videos": videos,
                },
            }

            db_movies.append(movie_data)
            
    print(page)

# JSON 파일로 저장
with open(
    "movies/fixtures/db_genres_providers_videos.json", "w", encoding="utf-8"
) as file:
    json.dump(db_genres_providers_videos, file, indent=4, ensure_ascii=False)

with open(
    "movies/fixtures/db_actors_directors_keywords.json", "w", encoding="utf-8"
) as file:
    json.dump(db_actors_directors_keywords, file, indent=4, ensure_ascii=False)

with open("movies/fixtures/db_movies.json", "w", encoding="utf-8") as file:
    json.dump(db_movies, file, indent=4, ensure_ascii=False)


print("JSON 파일 생성 완료: db_1.json, db_2.json, db_3.json")
