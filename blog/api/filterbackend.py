import coreapi
import coreschema

from django.utils.encoding import force_str
from django_restql.settings import restql_settings
from django.db.models import Avg
from rest_framework.filters import OrderingFilter


class PostOrderingFilterBackend(OrderingFilter):
    def filter_queryset(self, request, queryset, view):
        ordering = self.get_ordering(request, queryset, view)

        if ordering:
            if "stars" in ordering or "-stars" in ordering:
                queryset = queryset.annotate(stars=Avg("user_stars__stars"))

            return queryset.order_by(*ordering)

        return queryset


class RestQLFilterBackend:
    def filter_queryset(self, request, queryset, view):
        return queryset

    def get_schema_fields(self, view):
        assert coreapi is not None, "coreapi must be installed to use `get_schema_fields()`"
        assert coreschema is not None, "coreschema must be installed to use `get_schema_fields()`"
        return [
            coreapi.Field(
                name=restql_settings.QUERY_PARAM_NAME,
                required=False,
                location="query",
                schema=coreschema.String(
                    title=force_str(restql_settings.QUERY_PARAM_NAME),
                    description="More info: https://yezyilomo.github.io/django-restql/querying_data/",
                ),
            )
        ]

    def get_schema_operation_parameters(self, view):
        return [
            {
                "name": restql_settings.QUERY_PARAM_NAME,
                "required": False,
                "in": "query",
                "description": force_str(restql_settings.QUERY_PARAM_NAME),
                "schema": {"type": "string",},
            },
        ]
