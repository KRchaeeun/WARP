from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, get_list_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth import logout

# authentication_classes Decorators
from rest_framework.decorators import authentication_classes
from rest_framework.authentication import TokenAuthentication, BasicAuthentication

# # permission Decorators
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser

# serializers
from .serializers import (
    UserFollowListSerializers,
    WishListSerializer,
    LikeListSerializer,
    UserProfileSerializer,
)
from movies.serializers import MovieSerializer

# Model
from .models import Wishlist, Movie, Like, User


# Create your views here.


@authentication_classes([TokenAuthentication])
@api_view(["GET", "POST"])
def follow(request, username):
    user = get_object_or_404(get_user_model(), username=username)

    if request.method == "GET":
        if user.followers.filter(pk=request.user.pk).exists():
            followed = True
        else:
            followed = False

    elif request.method == "POST":
        if user != request.user:
            if user.followers.filter(pk=request.user.pk).exists():
                user.followers.remove(request.user)
                followed = False
            else:
                user.followers.add(request.user)
                followed = True

    context = {
        "followed": followed,
        # postman 확인용
        # "request.user": request.user.pk,
    }
    # return redirect('accounts:profile', user.username)
    return Response(context, status=status.HTTP_200_OK)


# 팔로우 목록
@api_view(["GET"])
# @permission_classes([IsAuthenticated])
def get_followers(request, username):
    user = get_object_or_404(get_user_model(), username=username)
    followers = user.followers.all()
    serializers = UserFollowListSerializers(followers, many=True)

    return Response(serializers.data, status=status.HTTP_200_OK)


# 팔로잉 목록
@api_view(["GET"])
# @permission_classes([IsAuthenticated])
def get_followings(request, username):
    user = get_object_or_404(get_user_model(), username=username)
    followings = user.followings.all()
    serializers = UserFollowListSerializers(followings, many=True)

    return Response(serializers.data, status=status.HTTP_200_OK)


# POST: wishlist 추가/삭제
@api_view(["POST"])
def wishlist(request, movie_id):
    # POST: wishlist 추가/삭제
    movie = get_object_or_404(Movie, pk=movie_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user, movie=movie)

    if not created:
        # 이미 찜 목록에 있으면 삭제
        wishlist.delete()
        return Response({"status": "removed from wishlist"}, status=status.HTTP_200_OK)
    else:
        # 찜 목록에 없으면 추가
        return Response({"status": "added to wishlist"}, status=status.HTTP_201_CREATED)


# GET: wishlist 조회
@api_view(["GET"])
def get_like(request, username):
    # username에 해당하는 사용자를 조회
    user = get_object_or_404(User, username=username)
    print(user)

    # 해당 사용자가 좋아하는 영화의 목록을 조회
    likes = user.liked_movies.all()

    # Serialize하여 JSON 응답으로 반환
    serializer = LikeListSerializer(likes, many=True)
    return Response(serializer.data)


# POST: like 추가/삭제
@api_view(["POST"])
def movie_like(request, movie_id):
    # POST: like 추가/삭제
    movie = get_object_or_404(Movie, pk=movie_id)
    like, created = Like.objects.get_or_create(user=request.user, movie=movie)

    if not created:
        # 이미 찜 목록에 있으면 삭제
        like.delete()
        return Response({"status": "removed from like"}, status=status.HTTP_200_OK)
    else:
        # 찜 목록에 없으면 추가
        return Response({"status": "added to like"}, status=status.HTTP_201_CREATED)


# GET: like 조회
@api_view(["GET"])
def get_wishlist(request, username):
    # username에 해당하는 사용자를 조회
    user = get_object_or_404(User, username=username)

    # 해당 사용자의 위시리스트 조회
    wishlist = user.wishlist.all()

    # Serialize하여 JSON 응답으로 반환
    serializer = LikeListSerializer(wishlist, many=True)
    return Response(serializer.data)


# GET: profile 조회
from django.http import Http404


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def profile(request, username):
    try:
        # 요청한 username에 해당하는 사용자의 프로필 정보 가져오기
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise Http404("사용자가 존재하지 않습니다.")
    # Serialize하여 JSON 응답으로 반환
    serializer = UserProfileSerializer(user)
    return Response(serializer.data)


# POST : 회원 탈퇴
@api_view(["POST"])
def delete_user_account(request):
    user = request.user
    if user.is_authenticated:
        logout(request)  # 사용자 로그아웃
        user.delete()
        return JsonResponse(
            {"message": "Account deleted successfully"}, status=status.HTTP_200_OK
        )
    return JsonResponse(
        {"error": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED
    )


# # GET: 로그인 된 user의 like, wishlist 조회
# @api_view(["GET"])
# def like_wishlist_recommendations(request):
#     liked_movies = (
#         Like.objects.filter(user=request.user)
#         .order_by("-id")
#         .values_list("movie", flat=True)
#     )
#     wishlist_movies = (
#         Wishlist.objects.filter(user=request.user)
#         .order_by("-id")
#         .values_list("movie", flat=True)
#     )
#     # context = {
#     #     {"liked_movies": list(liked_movies), "wishlist_movies": list(wishlist_movies)}
#     # }
#     # return context
#     return JsonResponse(
#         {"liked_movies": list(liked_movies), "wishlist_movies": list(wishlist_movies)}
#     )


# GET: 로그인 된 user의 like, wishlist 조회
@api_view(["GET"])
def like_wishlist_recommendations(request, username):
    liked_movies = (
        Like.objects.filter(user=request.user)
        .order_by("-id")
        .values_list("movie", flat=True)
    )
    wishlist_movies = (
        Wishlist.objects.filter(user=request.user)
        .order_by("-id")
        .values_list("movie", flat=True)
    )

    # liked_movies와 wishlist_movies에서 각각 하나씩 선택
    liked_movie = list(liked_movies)[:1]  # 첫 번째 liked_movie (빈 리스트면 [])
    wishlist_movie = list(wishlist_movies)[:1]  # 첫 번째 wishlist_movie (빈 리스트면 [])

    # 빈 리스트의 경우 None으로 대체
    liked_movie = liked_movie[0] if liked_movie else None
    wishlist_movie = wishlist_movie[0] if wishlist_movie else None

    return JsonResponse({"liked_movie": liked_movie, "wishlist_movie": wishlist_movie})


from django.db.models import Count
from movies.models import Genre


@api_view(["GET"])
def get_most_common_genre_for_user(request):
    # user의 위시리스트에 있는 영화들의 장르를 조회
    wishlist_movies_genres = (
        Genre.objects.filter(movie__wishlist__user=request.user)
        .annotate(num_movies=Count("movie"))
        .order_by("-num_movies")
    )

    # 가장 많이 나타나는 장르 반환
    if wishlist_movies_genres:
        return JsonResponse(
            {"wishlist_movies_genres": wishlist_movies_genres.first().name}
        )
    else:
        return None
