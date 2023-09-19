from django.shortcuts import render ,get_object_or_404
from .models import *
from .serializers import *
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, GenericAPIView, ListCreateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from datetime import datetime
from rest_framework.permissions import IsAuthenticated
import socket

from django.http import HttpRequest

def get_client_ip(request: HttpRequest) -> str:
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip_list = x_forwarded_for.split(',')
        return ip_list[0].strip()
    return request.META.get('REMOTE_ADDR')


# 소통해요 글 리스트 보기, 소통해요 글 생성하기, 글 상세보기, 수정하기, 삭제하기
class PostModelViewSet(ModelViewSet):
    queryset=Post.objects.all()

    # 시리얼라이저 선택
    def get_serializer_class(self):
        # get 요청일 경우 (리스트를 조회하는 우)
        if self.action=='list':
            return PostListSerializer
        elif self.action=='retrieve':
            return PostRetreiveSerializer
        else:
            return PostCreateSerializer
        
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # author 필드를 유효성 검사 이후 따로 넣어줘야 함 

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    # 전체 경로 말고, 이미지 경로만 나오도록 
    def get_serializer_context(self):
        return {
            'request': None,
            'format': self.format_kwarg,
            'view': self
        }
    
# 소통해요 게시물에 답글 달기, 
class CommentModelViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    # 애초에 로그인 한 사용자만 사용 가능 
    
    def get_serializer_class(self):
        if self.request.method in ['GET', 'RETRIEVE']:
            return CommentListRetrieveSerializer
        else:
            return GuestCreateUpdateSerializer
    def list(self, request, *args, **kwargs):
        return Response(status=status.HTTP_404_NOT_FOUND)

    def create(self, request,post_pk, *args, **kwargs):
        post_pk = Post.objects.get(id=post_pk)  # URL에서 게시물의 ID를 가져옴
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # author 필드를 유효성 검사 이후 따로 넣어줘야 함 
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
    

    