from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt


def health_check(request):
    return JsonResponse({"status": "ok", "service": "django_core"})


urlpatterns = [
    path("admin/", admin.site.urls),
    path("health/", health_check),
    path("api/health/", health_check),
    path("api/v1/", include("config.api_v1_urls")),
    path("api/v1/graphql/", csrf_exempt(GraphQLView.as_view(graphiql=True))),
]