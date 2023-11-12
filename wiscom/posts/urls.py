from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'posts', PostModelViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # 다른 URL 패턴들...
]
urlpatterns+=[
    path('posts/<int:id>/like/', PostLikeShowAPIView.as_view(), name='like_post'),
    path('posts/<int:id>/like/add/', PostLikeAPIView.as_view())
]
# 중첩된 라우팅을 수행
post_router = DefaultRouter()
post_router.register(r'comments', CommentModelViewSet, basename='comment')

urlpatterns += [
    path('posts/<int:post_pk>/', include(post_router.urls)),
]