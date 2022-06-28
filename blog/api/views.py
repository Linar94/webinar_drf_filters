from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from posts.models import Comment, Post, Follow, Star
from .filterbackend import PostOrderingFilterBackend, RestQLFilterBackend
from .filtersets import PostFilterSet

from .serializers import (
    CommentSerializer, PostSerializer, UserSerializer, StarSerializer
)


class PostViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    queryset = Post.objects.select_related("group").prefetch_related("user_stars")
    serializer_class = PostSerializer

    permission_classes = (IsAuthenticated,)
    http_method_names = ["get", "post", "patch"]

    filter_backends = (SearchFilter, DjangoFilterBackend, PostOrderingFilterBackend, RestQLFilterBackend)
    filterset_class = PostFilterSet
    search_fields = ["topic", "=author__username"]
    ordering_fields = ["pub_date", "topic", "stars"]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @swagger_auto_schema(responses={status.HTTP_200_OK: UserSerializer()}, operation_description="Get all followers by post's author")
    @action(
        methods=("GET",), url_path="followers", detail=True,
    )
    def followers(self, request, *args, **kwargs):
        followers = [f.user for f in self.get_object().author.following.all()]
        return Response(UserSerializer(followers, many=True).data)

    @swagger_auto_schema(responses={status.HTTP_200_OK: ""}, request_body=StarSerializer)
    @action(
        methods=("POST",), url_path="set-star", detail=True,
    )
    def set_star(self, request, *args, **kwargs):
        post = self.get_object()
        if StarSerializer(data=request.data).is_valid(raise_exception=True):
            Star.objects.update_or_create(post=post, user=request.user, defaults={"stars": request.data["stars"]})
        return Response(status=status.HTTP_200_OK)


class CommentViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated,)

    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ['post']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        return Comment.objects.select_related("post")
