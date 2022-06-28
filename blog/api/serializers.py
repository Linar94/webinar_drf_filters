from django.db.models import Avg
from django_restql.mixins import DynamicFieldsMixin
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import CurrentUserDefault

from posts.models import Comment, Follow, Group, Post, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("id", "first_name", "last_name")
        model = User


class PostSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    author_name = serializers.CharField(source="author", read_only=True)
    stars = serializers.SerializerMethodField()

    class Meta:
        fields = ("id", "pub_date", "topic", "author_name", "text", "group", "stars")
        model = Post

    def get_stars(self, obj):
        return obj.user_stars.aggregate(stars_avg=Avg("stars"))["stars_avg"] or 0

    # def to_representation(self, instance):
    #     res = super().to_representation(instance)
    #     res["group"] = GroupSerializer(instance=instance.group).data if instance.group else None
    #     return res


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )

    class Meta:
        fields = '__all__'
        model = Comment


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True, slug_field='username', default=CurrentUserDefault()
    )
    following = serializers.SlugRelatedField(
        read_only=False, slug_field='username',
        queryset=User.objects.all()
    )

    class Meta:
        model = Follow
        fields = ('user', 'following')


class StarSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    def validate(self, attrs):
        if attrs.get("stars") and attrs["stars"] > 5:
            raise ValidationError({"stars": "Максимальная оценка не должна превышать 5 звезд"})
        return attrs

    stars = serializers.IntegerField(required=True)
