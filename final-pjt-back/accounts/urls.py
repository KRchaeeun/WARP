from django.urls import path
from . import views

urlpatterns = [
    # ## Users ##
    # # GET: 모든 사용자 정보 조회 (admin)  # POST: 새로운 사용자 계정 생성 (회원가입)
    # # 'user_list_or_create' 대신 'users' 사용
    # path('users/', views.user_list_or_create, name='users'),
    # # GET: 사용자(본인) 프로필 조회  # PUT: 사용자(본인) 프로필 업데이트  # DELETE: 사용자 계정 삭제 (본인 혹은 admin)
    # # 'user_retrieve_update_delete' 대신 'user_detail' 사용
    # path('users/<int:user_id>/', views.user_retrieve_update_delete, name='user_detail'),
    # ## Email Verification ##
    # # POST: 인증 이메일 발송  # PUT: 토큰을 이용한 이메일 인증
    # # 'email_verify_or_send' 대신 'verify_email' 사용
    # path('verify/', views.email_verify_or_send, name='email_verify_or_send'),
    # # 토큰을 이용한 이메일 인증
    # # 'email_verify_with_token' 대신 'verify_token' 사용
    # path('verify/<str:token>/', views.email_verify_with_token, name='verify_token'),
    ## Follow ##
    # POST : 팔로우 언팔로우 가능
    path("user/<str:username>/follow/", views.follow, name="follow"),
    # GET : 특정 사용자의 팔로잉 목록 확인 가능
    path("<str:username>/followingslist/", views.get_followings),
    # GET : 특정 사용자의 팔로우 목록 확인 가능
    path("<str:username>/followerslist/", views.get_followers),
    # POST : 특정 영화에 대한 좋아요 추가/삭제
    path("movies/<int:movie_id>/like/", views.movie_like),
    # GET : 특정 사용자의 좋아하는 영화 목록 조회
    path("users/<str:username>/likelist/", views.get_like),
    # POST : 특정 영화에 대한 위시리스트 추가/삭제
    path("movies/<int:movie_id>/wishlist/", views.wishlist),
    # GET : 특정 사용자의 위시리스트 조회
    path("users/<str:username>/wishlistlist/", views.get_wishlist),
    # GET : profile 조회
    path("profile/<str:username>/", views.profile),
    # POST : 회원 탈퇴
    path("delete_account/", views.delete_user_account, name="delete_account"),
    # GET : 추천을 위한 정보 조회
    path(
        "like_wishlist_recommendations/<str:username>/",
        views.like_wishlist_recommendations,
    ),
    # GET : 추천을 위한 장르 조회
    path("get_genre", views.get_most_common_genre_for_user),
]
