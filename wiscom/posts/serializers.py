from rest_framework import serializers
from .models import Post, Comment

class PostListSerializer(serializers.ModelSerializer):
    tags = serializers.StringRelatedField(many=True)
    class Meta:
        model = Post
        fields = ['id','title','content','likes','tags']

class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title','content','tags']

class CommentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        exclude=['post']

class PostRetreiveSerializer(serializers.ModelSerializer):
    tags = serializers.StringRelatedField(many=True)
    comments = CommentListSerializer(many=True, read_only=True)
    class Meta:
        model=Post
        fields=['id','title','content','comments','tags']

class CommentCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model=Comment
        exclude = ['created_at', 'post']