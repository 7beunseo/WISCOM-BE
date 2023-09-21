from rest_framework import serializers
from .models import Post, Comment

class TagSerializer(serializers.StringRelatedField):
    def to_representation(self, value):
        return value.name
    
class PostListSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    class Meta:
        model = Post
        fields = ['id','title','content','likes','tags']

class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title','content','tags']

class CommentListSerializer(serializers.ModelSerializer):
    comment_tags = serializers.StringRelatedField(many=True)
    created_at = serializers.SerializerMethodField()

    def get_created_at(self, obj):
        return obj.created_at.strftime("%Y-%m-%d")
    class Meta:
        model = Comment
        exclude = ['post']


class PostRetreiveSerializer(serializers.ModelSerializer):
    tags = serializers.StringRelatedField(many=True)
    comments = CommentListSerializer(many=True, read_only=True)
    class Meta:
        model=Post
        fields=['id','title','content','comments','tags']

class CommentCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model=Comment
        fields=['content','comment_tags']
