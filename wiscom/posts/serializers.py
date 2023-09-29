from rest_framework import serializers
from .models import Post, Comment, CommentTag
from developers.models import Developer


class PostListSerializer(serializers.ModelSerializer):
    tags = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'title','team', 'likes', 'tags']
    
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
    images = serializers.SerializerMethodField()
    developer = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'title', 'team', 'images', 'content', 'comments', 'tags', 'likes', 'developer']

    # def get_queryset(self):
    #     number = self.context.get('id')  # 컨텍스트에서 'id' 값을 가져옵니다.
    #     return Post.objects.filter(id=number)  # 'id'로 필터링합니다.
    
    def get_developer(self, instance):
        # 'post_number'가 'id'와 일치하는 개발자를 필터링합니다.
        number = self.instance.id
        developers = Developer.objects.filter(post_number=number)
        return DeveloperSerializer(developers, many=True).data
    
    def get_images(self, post):
        photos_queryset = post.post_image.all()
        photos_urls = [photo.image.url for photo in photos_queryset]
        return photos_urls

    def get_tags(self, instance):
        posts = instance.tags.filter(category='posts')
        comments = instance.tags.filter(category='comments')
        return {"posts": posts.values_list('name', flat=True), "comments": comments.values_list('name', flat=True)}

class DeveloperSerializer(serializers.ModelSerializer):
    class Meta:
        model = Developer
        fields = ['name', 'image']

class CommentCreateUpdateSerializer(serializers.ModelSerializer):
    comment_tags = serializers.PrimaryKeyRelatedField(many=True, queryset=CommentTag.objects.all())

    class Meta:
        model = Comment
        fields = ['post_number', 'content', 'comment_tags']

