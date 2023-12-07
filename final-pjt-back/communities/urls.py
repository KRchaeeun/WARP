from django.urls import path
from . import views

urlpatterns = [
    ## Posts ##

    # GET: 모든 게시글 조회  # POST: 게시글 생성
    # 'post_list_or_create' 대신 'posts' 사용
    path('posts/', views.post_list_or_create, name='posts'),
    # GET: 단일 게시글 조회  # PUT: 단일 게시글 수정  # DELETE: 단일 게시글 삭제
    # 'post_retrieve_update_delete' 대신 'post_detail' 사용
    path('posts/<int:post_id>/', views.post_retrieve_update_delete, name='post_detail'),
    # 게시글 좋아요/좋아요 취소
    path('posts/<int:post_id>/like/', views.post_like_toggle, name='post_like_toggle'),

    ## Comments ##

    # GET: 게시글의 모든 댓글 조회  # POST: 게시글에 댓글 생성
    # 'comment_list_or_create' 대신 'comments' 사용
    path('posts/<int:post_id>/comments/', views.comment_list_or_create, name='comments'),
    # PUT: 단일 댓글 수정  # DELETE: 단일 댓글 삭제
    # 'comment_retrieve_update_delete' 대신 'comment_detail' 사용
    path('comments/<int:comment_id>/', views.comment_retrieve_update_delete, name='comment_detail'),
    # 댓글 좋아요/좋아요 취소
    path('comments/<int:comment_id>/like/', views.comment_like_toggle, name='comment_like_toggle'),
]
