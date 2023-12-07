from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from django.db.models import Count
from django.shortcuts import get_object_or_404

from .models import Community, Comment

from .serializers import CommunitySerializer, CommunityListSerializer, CommentSerializer
# # authentication_classes Decorators
# from rest_framework.decorators import authentication_classes
# from rest_framework.authentication import TokenAuthentication, BasicAuthentication
# # permission Decorators
# from rest_framework.decorators import permission_classes
# from rest_framework.permissions import IsAuthenticated, IsAdminUser


# GET: 모든 게시글 조회  # POST: 게시글 생성
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def post_list_or_create(request):
    # GET 요청 처리: 모든 게시글 조회
    if request.method == 'GET':
        communities = Community.objects.all() # 최신순 정렬
        serializer = CommunityListSerializer(communities, many=True)
        return Response(serializer.data)
    
    # POST 요청 처리: 새 게시글 생성
    elif request.method == 'POST':
        serializer = CommunitySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)  # 'user' 필드는 현재 로그인한 사용자로 설정
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# GET: 단일 게시글 조회  # PUT: 단일 게시글 수정  # DELETE: 단일 게시글 삭제
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def post_retrieve_update_delete(request, post_id):
    # 특정 게시글 인스턴스를 가져옴
    community = get_object_or_404(Community, pk=post_id)
    
    # GET 요청: 단일 게시글 조회
    if request.method == 'GET':
            serializer = CommunitySerializer(community)
            data = serializer.data
            # 현재 로그인한 사용자가 게시글에 좋아요를 눌렀는지 여부 추가
            data['user_has_liked'] = request.user in community.likes.all()
            return Response(data)
    
    # PUT 요청: 단일 게시글 수정
    elif request.method == 'PUT':
        print("Received PUT data:", request.data)
        serializer = CommunitySerializer(community, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # DELETE 요청: 단일 게시글 삭제
    elif request.method == 'DELETE':
        community.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# POST: 게시글 좋아요/좋아요 취소
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def post_like_toggle(request, post_id):
    post = get_object_or_404(Community, pk=post_id)
    user_has_liked = request.user in post.likes.all()

    if user_has_liked:
        post.likes.remove(request.user)
        post.like_count = post.likes.count()  # 좋아요 개수 업데이트
        action = "좋아요 취소"
    else:
        post.likes.add(request.user)
        post.like_count = post.likes.count()  # 좋아요 개수 업데이트
        action = "좋아요"

    post.save()  # 변경사항 저장

    return Response({
        'status': 'success',
        'action': action,
        'userHasLiked': user_has_liked,
        'likes_count': post.like_count,
    }, status=status.HTTP_200_OK)



# GET: 게시글의 모든 댓글 조회  # POST: 게시글에 댓글 생성
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def comment_list_or_create(request, post_id):
    # 해당 게시글 찾기
    post = get_object_or_404(Community, pk=post_id)
    
    # GET 요청: 해당 게시글의 모든 댓글 조회
    if request.method == 'GET':
        # 댓글을 좋아요 개수에 따라 정렬
        comments = Comment.objects.filter(post=post, parent_comment__isnull=True).annotate(like_count=Count('likes')).order_by('-like_count', '-created_at')
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
    
    # POST 요청: 새 댓글/대댓글 생성
    elif request.method == 'POST':
        parent_comment_id = request.data.get('parent_comment')
        parent_comment = None
        
        # 대댓글이라면
        if parent_comment_id:
            parent_comment = get_object_or_404(Comment, pk=parent_comment_id)
        serializer = CommentSerializer(data=request.data)
        
        # 댓글이라면 
        if serializer.is_valid():
            serializer.save(post=post, user=request.user, parent_comment=parent_comment)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# PUT: 단일 댓글 수정  # DELETE: 단일 댓글 삭제
@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def comment_retrieve_update_delete(request, comment_id):
    # 단일 댓글 인스턴스를 가져옴
    comment = get_object_or_404(Comment, pk=comment_id)

    # PUT 요청: 단일 댓글(또는 대댓글) 수정
    if request.method == 'PUT':
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # DELETE 요청: 단일 댓글(또는 대댓글) 삭제
    elif request.method == 'DELETE':
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# POST: 댓글 좋아요/좋아요 취소
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def comment_like_toggle(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    
    # 대댓글인 경우 좋아요 기능을 비활성화
    if comment.parent_comment:
        return Response({'error': 'Like not allowed on replies'}, status=status.HTTP_400_BAD_REQUEST)

    # 일반 댓글에 대한 좋아요/좋아요 취소 처리
    if request.user in comment.likes.all():
        comment.likes.remove(request.user)
    else:
        comment.likes.add(request.user)

    return Response({'status': 'success'}, status=status.HTTP_200_OK)