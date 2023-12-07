from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Wishlist, Like, User
from movies.serializers import MovieSerializer  # MovieSerializer 가져오기


User = get_user_model()


## 프로필 ##
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "profile_image",
            "followings",
            "followers",
            "wishlist_users",
            "liked_users",
        )


## 팔로우 ##


class UserFollowListSerializers(serializers.ModelSerializer):
    class UserListSerializers(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ("id", "username")

    followings = UserListSerializers(many=True)
    following_count = serializers.IntegerField(
        source="followings.count", read_only=True
    )
    followers = UserListSerializers(many=True)
    follower_count = serializers.IntegerField(source="followers.count", read_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "followers",
            "follower_count",
            "followings",
            "following_count",
        )


## 위시리스트 ##
class WishListSerializer(serializers.ModelSerializer):
    movie = MovieSerializer(read_only=True)  # Movie 정보 포함
    
    class Meta:
        model = Like
        fields = ('user', 'movie')


## like ##
class LikeListSerializer(serializers.ModelSerializer):
    movie = MovieSerializer(read_only=True)  # Movie 정보 포함

    class Meta:
        model = Like
        fields = ('user', 'movie')