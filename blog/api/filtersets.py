from django_filters import BaseCSVFilter, FilterSet

from posts.models import Post, Group


class PostFilterSet(FilterSet):
    authors_or = BaseCSVFilter(method="filter_authors_or")

    class Meta:
        model = Post
        fields = ("author", "group__slug", "user_stars__user")

    def filter_authors_or(self, qs, name, value):
        return qs.filter(author_id__in=value)
