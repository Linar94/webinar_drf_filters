from django.urls import include, path

from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

from blog.yasg import get_schema
from .views import CommentViewSet, PostViewSet

v1_router = DefaultRouter()
v1_router.register('post', PostViewSet, basename='v1_post')
v1_router.register('comment', CommentViewSet, basename='v1_comment')

jwt_patterns = [
    path('create/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('verify/', TokenVerifyView.as_view(), name='token_verify'),
]

urlpatterns = v1_router.urls + [path('jwt/', include(jwt_patterns))]

urlpatterns += (
    path("swagger-ui/", get_schema(urlpatterns).with_ui("swagger", cache_timeout=0), name="schema-swagger-ui",),
    path('redoc/', get_schema(urlpatterns).with_ui('redoc', cache_timeout=0), name='schema-redoc'),
)