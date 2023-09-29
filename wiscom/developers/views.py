from rest_framework import generics
from .models import Developer
from .serializers import DeveloperSerializer

class DeveloperListCreateView(generics.ListCreateAPIView):
    queryset = Developer.objects.all()
    serializer_class = DeveloperSerializer