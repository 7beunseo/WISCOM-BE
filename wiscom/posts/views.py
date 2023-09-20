from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend 
from django.http import HttpRequest
from .serializers import PostListSerializer, PostCreateSerializer, CommentListSerializer, PostRetreiveSerializer, CommentCreateUpdateSerializer
from .models import Post,Comment, Like

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

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

        
class PostLikeAPIView(GenericAPIView):
    def get(self, request, post_id, *args, **kwargs):
        post = Post.objects.get(id=post_id)
        
        ip = get_client_ip(request)
        print(ip)

        # 해당 게시물에 대한 좋아요가 이미 있는지 확인
        existing_like = Like.objects.filter(post=post, ip=ip)

        if existing_like:
            # 이미 좋아요를 눌렀으면 아무 작업도 하지 않음
            response_data = {
                        'message': '이미 좋아요를 눌렀습니다.'
                    }
        else:
            # 좋아요를 생성하고 게시물의 좋아요 수를 증가
            Like.objects.create(post=post, ip=ip)
            post.likes += 1
            post.save()
            response_data = {
                        'message': '좋아요가 추가되었습니다.'
                    }
            
        return Response(response_data)
    

    