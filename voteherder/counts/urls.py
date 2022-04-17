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

router = routers.DefaultRouter()
router.register(r"users", UserViewSet)
router.register(r"groups", GroupViewSet)
router.register(r"elections", ElectionViewSet)
router.register(r"candidates", CandidateViewSet)
router.register(r"stages", StageViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path("", include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]
