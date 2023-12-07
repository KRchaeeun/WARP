from rest_framework import serializers

from django.contrib.auth import get_user_model

from .models import Genre, Video, Movie, Review


# 유저 정보
User = get_user_model()

class UserSerializer(serializers.ModelSerializer): 
    
    class Meta:
        model = User
        fields = ('id', 'username',)


# 영화 장르 정보
class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'
        
        

# 영화 티저 영상 정보
class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = '__all__'
        


# 전체 영화 정보 
class MovieListSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, read_only=True)  # 장르 정보 포함
    videos = VideoSerializer(many=True, read_only=True)  # 티저 영상 정보 포함
    class Meta:
        model = Movie
        fields = ('id', 'title', 'poster_path', 'genres', 'videos',)  # lee: 어떤 정보를 사용할지 정하기


# 단일 영화 정보
class MovieSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, read_only=True)
    videos = VideoSerializer(many=True, read_only=True)
    
    # 해당 영화의 리뷰
    class ReviewListSerializer(serializers.ModelSerializer):
        user = UserSerializer(read_only=True)
        class Meta:
            model = Review
            fields = '__all__'
    
    class Meta:
        model = Movie
        fields = '__all__'
            
    review_set = ReviewListSerializer(many=True, read_only=True)  # 해당 영화의 리뮤 목록
    review_count = serializers.IntegerField(source='review_set.count', read_only=True)  # 해당 영화에 대한 리뷰의 총 개수
        

# 리뷰 정보
class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Review
        fields = '__all__'
        extra_kwargs = {'movie': {'read_only': True}}