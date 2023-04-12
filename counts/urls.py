from django.urls import include, path, re_path
from django.views.generic import TemplateView
from rest_framework import routers

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


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
    StageDetailView,
    BallotViewSet,
)


api_router = routers.SimpleRouter()
api_router.register(r"users", UserViewSet)
api_router.register(r"groups", GroupViewSet)
api_router.register(r"election", ElectionViewSet)
api_router.register(r"ballot", BallotViewSet)
api_router.register(r"candidate", CandidateViewSet)
api_router.register(r"stage", StageViewSet)

schema_view = get_schema_view(
    openapi.Info(
        title="VoteHerder API",
        default_version="v1",
        description="VoteHerder API",
        terms_of_service="https://www.voteherder.org/policies/terms/",
        contact=openapi.Contact(email="contact@voteherder.org"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path("about/", TemplateView.as_view(template_name="about.html"), name="about"),
    path("election/", ElectionListView.as_view(), name="election"),
    path("election/<str:pk>", ElectionDetailView.as_view(), name="election-detail"),
    path("candidate/", CandidateListView.as_view(), name="election"),
    path("candidate/<int:pk>", CandidateDetailView.as_view(), name="candidate-detail"),
    path("stage/<uuid:pk>", StageDetailView.as_view(), name="stage-detail"),
    path("api/v1/", include(api_router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    re_path(
        r"^swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    re_path(
        r"^redoc/$", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"
    ),
]
