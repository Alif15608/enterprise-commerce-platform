from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView


def health_check(request):
    return JsonResponse({"status": "ok", "service": "django_core"})


urlpatterns = [
    path("admin/", admin.site.urls),
    path("health/", health_check),
    path("api/health/", health_check),
    path("api/v1/", include("config.api_v1_urls")),
    path("api/v1/graphql/", csrf_exempt(GraphQLView.as_view(graphiql=True))),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
