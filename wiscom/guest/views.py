from collections import OrderedDict

from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.response import Response

from .serializers import CommentSerializer
from .models import Guest
from rest_framework.pagination import PageNumberPagination


# Create your views here.
class GuestListCreateView(generics.ListCreateAPIView):
    queryset = Guest.objects.all()
    serializer_class = CommentSerializer
    pagination_class = PageNumberPagination  # 페이지네이션 클래스 설정

class GuestViewSet(viewsets.ModelViewSet):
    queryset = Guest.objects.all()
    serializer_class=CommentSerializer
    def get_queryset(self):
        return Guest.objects.all().order_by('-id')

class PostPageNumberPagination(PageNumberPagination):
    page_size = 6
    # page_size_query_param = 'page_size'
    # max_page_size = 1000
    def get_paginated_response(self, data):
        return Response(OrderedDict([  
            ('postList', data),
            ('pageCnt', self.page.paginator.count), 
            ('curPage', self.page.paginator.count),
        ]))