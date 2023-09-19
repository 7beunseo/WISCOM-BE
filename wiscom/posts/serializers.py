from rest_framework import serializers
from .models import *

# 소통해요에 올라온 글 리스트
class PostListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ['title','content','likes']

# 소통해요에 글 작성
class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title','content']

# 소통해요 글 상세보기를 누르면, 해당 게시물에 달린 댓글 리스트를 보여줌 
class CommentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        exclude=['post']

# 소통해요 글 상세보기 
class PostRetreiveSerializer(serializers.ModelSerializer):
    comments = CommentListSerializer(many=True, read_only=True)
    class Meta:
        model=Post
        fields=['title','content','comments']


# 답글 글 조회, 상세보기 
class CommentListRetrieveSerializer(serializers.ModelSerializer):
		# author의 이름이 출력되도록 함 > 익명으로 바꿀건지?
    class Meta:
        model=Comment
        fields='__all__'

# 답글 생성, 수정
class GuestCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model=Comment
				# 직접 작성하는 필드는 제목, 내용뿐
        exclude = ['created_at', 'post']

class PostLikeSerializer(serializers.ModelSerializer):
    class Mdeta:
        model=Post
        include=('like',)