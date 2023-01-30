from django.urls import include, path, re_path
from django.views.generic import TemplateView
from rest_framework import routers

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


from .views import (
    ElectionListView,
    ElectionDetailView,
    CandidateListView,
    CandidateDetailView,
    StageDetailView, 
)

app_name = "counts"

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path("about/", TemplateView.as_view(template_name="about.html"), name="about"),
    path("election/", ElectionListView.as_view(), name="election-list"),
    path("election/<str:pk>", ElectionDetailView.as_view(), name="election-detail-pk"),
    path("candidate/", CandidateListView.as_view(), name="candidate"),
    path("candidate/<int:pk>", CandidateDetailView.as_view(), name="candidate-detail-pk"),
    path("stage/<uuid:pk>", StageDetailView.as_view(), name="stage-detail-pk"),
]
