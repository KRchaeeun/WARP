from django.db import models
from django.conf import settings

## Community 모델 ##

class Community(models.Model):
    # 커뮤니티 글 작성자
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_communities')
    # 커뮤니티 글 제목
    title = models.CharField(max_length=100)
    # 커뮤니티 글 내용
    content = models.TextField()
    # 커뮤니티 글 생성 일시
    # auto_now_add=True : 레코드가 생성될 때 자동으로 현재 일시로 설정
    created_at = models.DateTimeField(auto_now_add=True)
    # 커뮤니티 글의 좋아요 중개 모델 생성
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_community')  # 모델 추가
    like_count = models.IntegerField(default=0)  # 좋아요 개수 필드



## Comment 모델 ##

class Comment(models.Model):
    # 댓글 작성 할 커뮤니티 글
    post = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='community_comment')
    # 댓글 작성자
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_comment')
    # 부모 댓글
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    # 댓글 내용
    content = models.TextField()
    # 댓글 생성 일시
    # auto_now_add=True : 레코드가 생성될 때 자동으로 현재 일시로 설정
    created_at = models.DateTimeField(auto_now_add=True)
    # 댓글의 좋아요 중개 모델 생성
    # Issue: 댓글의 좋아요인지, Community의 좋아요인지 확인 필요
    # -> 두 모델 모두 필요
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_comments')
