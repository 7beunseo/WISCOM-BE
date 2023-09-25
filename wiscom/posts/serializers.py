from rest_framework import serializers
from .models import Post, Comment, CommentTag


class PostListSerializer(serializers.ModelSerializer):
    tags = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'likes', 'tags']
    
    def get_tags(self, instance):
        posts = instance.tags.filter(category='posts')
        comments = instance.tags.filter(category='comments')
        return {"posts": posts.values_list('name', flat=True), "comments": comments.values_list('name', flat=True)}


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
    tags = serializers.SerializerMethodField()
    comments = CommentListSerializer(many=True, read_only=True)
    likes = serializers.IntegerField()

    class Meta:
        model=Post
        fields=['id','title','content','comments','tags', 'likes']

    def get_tags(self, instance):
        posts = instance.tags.filter(category='posts')
        comments = instance.tags.filter(category='comments')
        return {"posts": posts.values_list('name', flat=True), "comments": comments.values_list('name', flat=True)}


class CommentCreateUpdateSerializer(serializers.ModelSerializer):
    comment_tags = serializers.PrimaryKeyRelatedField(many=True, queryset=CommentTag.objects.all())

    class Meta:
        model = Comment
        fields = ['content', 'comment_tags']

