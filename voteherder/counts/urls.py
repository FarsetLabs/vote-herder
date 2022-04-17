from django.urls import include, path
from rest_framework import routers

from .views import (
    ElectionViewSet,
    CandidateViewSet,
    StageViewSet,
    UserViewSet,
    GroupViewSet,
)

app_name = "counts"

api_router = routers.DefaultRouter()
api_router.register(r"users", UserViewSet)
api_router.register(r"groups", GroupViewSet)
api_router.register(r"elections", ElectionViewSet)
api_router.register(r"candidates", CandidateViewSet)
api_router.register(r"stages", StageViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path("api/v1/", include(api_router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]
