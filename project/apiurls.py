from django.urls import path
from . import apiviews
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Setup Swagger schema view
schema_view = get_schema_view(
    openapi.Info(
        title="PHI API",
        default_version='v1',
        description="this is our all api",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@myapi.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
)

urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-ui'),
    path('', apiviews.index, name='language'),  # Ensure 'index' exists in apiviews
    path('lang', apiviews.GetLanguages, name='getlang')
]
