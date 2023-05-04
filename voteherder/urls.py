"""voteherder URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include
from django.urls import path

import voteherder.settings as settings
from voteherder.utils import print_url_pattern_names
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
    BallotViewSet,
    ElectionListView,
    CandidateListView,
    ElectionDetailView,
    CandidateDetailView,
    StageDetailView
)


api_router = routers.DefaultRouter()
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
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
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


if settings.DEBUG:
    print_url_pattern_names(urlpatterns)