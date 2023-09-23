from django.urls import path, include
from .views import GuestListCreateView
from rest_framework.routers import DefaultRouter
from guest import views  # guest 앱의 views를 import합니다.


router = DefaultRouter()
router.register(r'guests', views.GuestViewSet)

urlpatterns = [
    # path('guests/', GuesctListCreateView.as_view(), name='guests-list-create'),
    path('', include(router.urls)),

]