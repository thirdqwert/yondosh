from django.urls import path, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from drf_yasg.generators import OpenAPISchemaGenerator


class HttpsSchemaGenerator(OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=False):
        schema = super().get_schema(request=request, public=public)
        schema.schemes = ["https"]  # принудительно HTTPS
        return schema

# Настраиваем Swagger документацию
schema_view = get_schema_view(
    openapi.Info(
        title="API Документация",        # Заголовок в Swagger UI
        default_version='v1',            # Версия API
        description="Описание API",      # Описание (можно указать как пользоваться API)
    ),
    public=True,                         # Доступ к документации открыт
    permission_classes=(permissions.AllowAny,),  # Любой может смотреть документацию
)

# Роуты для Swagger
urlpatterns = [
    # JSON и YAML схемы (для экспорта)
    re_path(
        r'^swagger(?P<format>\.json|\.yaml)$',
        schema_view.without_ui(cache_timeout=0),
        name='schema-json'
    ),

    # UI-версия (удобный интерфейс Swagger)
    path(
        'swagger/',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui'
    ),
]



