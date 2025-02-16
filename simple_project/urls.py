from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.http import JsonResponse

def health_check(request):
    return JsonResponse({"status": "healthy"})

schema_view = get_schema_view(
    openapi.Info(
        title="Backend Onboarding Challenge API",
        default_version='v1',
        description="백엔드 온보딩 챌린지 API 문서",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
)

urlpatterns = [
    # API endpoints
    path('accounts/', include('accounts.urls')),
    
    # Documentation
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    
    # Root URL shows Swagger UI
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='root'),
    
    # Health check endpoint
    path('health/', health_check, name='health_check'),
]
