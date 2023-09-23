from django.shortcuts import render
from rest_framework import generics, viewsets
from .serializers import CommentSerializer
from .models import Guest

# Create your views here.
class GuestListCreateView(generics.ListCreateAPIView):
    queryset = Guest.objects.all()
    serializer_class = CommentSerializer

class GuestViewSet(viewsets.ModelViewSet):
    queryset = Guest.objects.all()
    serializer_class=CommentSerializer
