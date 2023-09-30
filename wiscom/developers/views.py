from rest_framework import generics
from .models import Developer
from .serializers import DeveloperSerializer

class DeveloperListCreateView(generics.ListCreateAPIView):
    queryset = Developer.objects.all()
    serializer_class = DeveloperSerializer

    def get_serializer_context(self):
        return {
            'request': None, #None으로 수정 
            'format': self.format_kwarg,
            'view': self
        }