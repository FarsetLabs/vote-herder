from django.urls import include, path
from django.views.generic import TemplateView
from rest_framework import routers

from .views import (
    ElectionViewSet,
    CandidateViewSet,
    StageViewSet,
    UserViewSet,
    GroupViewSet,
    ElectionListView,
    ElectionDetailView,
    CandidateListView,
    CandidateDetailView,
    StageDetailView
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
    path("", TemplateView.as_view(template_name="home.html"), name='home'),
    path("about/", TemplateView.as_view(template_name="about.html"), name='about'),
    path("election/", ElectionListView.as_view(), name='election'),
    path("election/<str:pk>", ElectionDetailView.as_view(), name='election-detail'),
    path("candidate/", CandidateListView.as_view(), name='election'),
    path("candidate/<int:pk>", CandidateDetailView.as_view(), name='candidate-detail'),
    path("stage/<uuid:pk>", StageDetailView.as_view(), name='stage-detail'),
    path("api/v1/", include(api_router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]
