from rest_framework import serializers

from django.contrib.auth import get_user_model

from .models import Community, Comment


# 유저 정보
User = get_user_model()

class UserSerializer(serializers.ModelSerializer): 
    
    class Meta:
        model = User
        fields = ('id', 'username',)


# 전체 게시글 정보

class CommunityListSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Community
        fields = ('id', 'user', 'title', 'created_at', 'likes', 'like_count')


# 댓글 정보
class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    post = serializers.PrimaryKeyRelatedField(read_only=True)
    likes = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    parent_comment = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'post', 'user', 'parent_comment', 'content', 'created_at', 'likes']



# 단일 게시글 정보
class CommunitySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    likes = serializers.PrimaryKeyRelatedField(many=True, read_only=True, required=False)

    class Meta:
        model = Community
        fields = ('id', 'user', 'title', 'content', 'created_at', 'likes', 'like_count')
        extra_kwargs = {'title': {'required': True}, 'content': {'required': True}}
