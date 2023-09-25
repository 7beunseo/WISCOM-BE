from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend 
from django.http import HttpRequest
from .serializers import PostListSerializer, PostCreateSerializer, CommentListSerializer, PostRetreiveSerializer, CommentCreateUpdateSerializer
from .models import Post,Comment, Like, Tag

def get_client_ip(request: HttpRequest) -> str:
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip_list = x_forwarded_for.split(',')
        return ip_list[0].strip()
    return request.META.get('REMOTE_ADDR')

class PostModelViewSet(ModelViewSet):
    queryset=Post.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['tags']
    search_fields = ['title']

    def get_serializer_class(self):
        if self.action=='list':
            return PostListSerializer
        elif self.action=='retrieve':
            return PostRetreiveSerializer
        else:
            return PostCreateSerializer
        
    def list(self, request):
        posts = Post.objects.all()
        serializer = PostListSerializer(posts, many=True)
        data = serializer.data
        return Response(data)
        
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    

class CommentModelViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    
    def get_serializer_class(self):
        if self.request.method in ['GET', 'RETRIEVE']:
            return CommentListSerializer
        else:
            return CommentCreateUpdateSerializer
        
    def list(self, request, *args, **kwargs):
        return Response(status=status.HTTP_404_NOT_FOUND)

    def create(self, request,post_pk, *args, **kwargs):
        post_pk = Post.objects.get(id=post_pk)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['post'] = post_pk  # 게시물의 ID를 post 필드에 저장

        comment_tags = serializer.validated_data.get('comment_tags', [])  # 시리얼라이저를 통해 들어온 comment_tag의 리스트를 가져옴 

        existing_hashtags = []
        for comment in post_pk.comments.all():  # 모든 댓글 반복 
            for tags in comment.comment_tags.all():  # 각각의 댓글에 달린 태그 
                existing_hashtags.append(tags) # 태그리스트에 추가  

        total_tags = comment_tags+existing_hashtags
        set_total_tags = set(total_tags)

        for hashtag in set_total_tags:
            hashtag_count = total_tags.count(hashtag)
            if hashtag_count >= 3:
                hashtag_object, created = Tag.objects.get_or_create(name=hashtag, category='comments')  # 태그의 객체를 생성한 후 넣어야 한다 
                post_pk.tags.add(hashtag_object)
            
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

        
class PostLikeAPIView(GenericAPIView):
    queryset = Post.objects.all()
    lookup_field = 'id' 

    def get(self, request, id, *args, **kwargs):
        liked_key = 'liked_post_{}'.format(id)

        if request.session.get(liked_key, False):
            return Response({"message": "이미 좋아요를 눌렀습니다."}, status=200)

        try:
            post = self.get_object()
        except Post.DoesNotExist:
            return Response({"error": "해당하는 게시물이 존재하지 않습니다."}, status=400)

        request.session[liked_key] = True

        Like.objects.create(post=post, ip=request.META.get('REMOTE_ADDR'))
        post.likes += 1
        post.save()
        return Response({"message": "좋아요가 추가되었습니다."}, status=400)