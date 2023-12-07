from django.db import models
from movies.models import Movie
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.conf import settings


## User Model ##


class User(AbstractUser):
    # AbstractUser 클래스의 주요 필드
    # username: 사용자의 고유한 식별자로 사용되는 사용자 이름
    # password: 사용자의 비밀번호를 저장하는 필드
    # email: 사용자의 이메일 주소를 저장하는 필드
    # first_name: 사용자의 이름을 저장하는 필드
    # last_name: 사용자의 성을 저장하는 필드
    # is_active: 사용자 계정이 활성화되었는지 여부를 나타내는 필드
    # is_staff: 사용자가 관리자 페이지에 로그인할 수 있는지 여부를 나타내는 필드
    # date_joined: 사용자가 가입한 일자를 저장하는 필드
    # last_login: 사용자가 마지막으로 로그인한 시간을 기록하는 필드

    # 유저 프로필이미지
    # Issue: profile ImageField와 CharField 선택 필요
    # -> ImageField는 사용자가 많을 때 이미지가 용량이 많이 필요하고
    #    CharField는 경로로 설정하므로 용량이 많이 필요하지 않지만 다른 저장소가 필요해 코드 복잡할 가능성 존재
    #    유저수도 적고 시간적 제한으로 인해 ImageField 사용하기로 결정
    profile_image = models.ImageField(
        upload_to="profile_images/", null=True, blank=True
    )
    # 유저 팔로우, 팔로잉
    followings = models.ManyToManyField(
        "self", symmetrical=False, related_name="followers"
    )
    # wishlist 중개모델 생성
    wishlist_users = models.ManyToManyField("self", through="Wishlist")
    # like 중개모델 생성
    liked_users = models.ManyToManyField("self", through="Like")

    groups = models.ManyToManyField(Group, related_name="user_groups")
    user_permissions = models.ManyToManyField(
        Permission, related_name="user_permissions"
    )


## Wishlist 모델 ##


class Wishlist(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="wishlist"
    )
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)


## Like 모델 ##


class Like(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="liked_movies"
    )
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
