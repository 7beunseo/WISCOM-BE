from django.urls import path
from .views import DeveloperListCreateView

urlpatterns = [
    path('developers/', DeveloperListCreateView.as_view(), name='developers'),
]