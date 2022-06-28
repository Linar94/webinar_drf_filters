from drf_yasg.generators import OpenAPISchemaGenerator
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from drf_yasg.views import get_schema_view
from drf_yasg import openapi


class SchemaGenerator(OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=False):
        schema = super().get_schema(request, public)
        schema.host = "127.0.0.1:8000"
        schema.base_path = "/api/v1"
        schema.schemes = ["http"]
        schema.schemes.reverse()
        return schema


def get_schema(urlpatterns):
    return get_schema_view(
        openapi.Info(
            title="Blog API",
            default_version='v1',
            description="Description",
        ),
        public=True,
        generator_class=SchemaGenerator,
        permission_classes=(IsAuthenticatedOrReadOnly,),
        patterns=urlpatterns,
    )