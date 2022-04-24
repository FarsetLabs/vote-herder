# Create your views here.

from django.contrib.auth.models import User, Group
from django.views.generic import ListView, DetailView
from rest_framework import permissions
from rest_framework import viewsets

from .models import Election, Candidate, Stage, StageCell, Ballot
from .serializers import (
    UserSerializer,
    GroupSerializer,
    ElectionSerializer,
    CandidateSerializer,
    StageSerializer,
    BallotSerializer,
)


### Default Viewsets provided via Auth
# todo should probably be moved into the base app / demo / whatever


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


### Count Viewsets


class ElectionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows elections to be viewed or edited.
    """

    lookup_field = "id"
    lookup_value_regex = "[a-z0-9.\-_]+"
    queryset = Election.objects.all().order_by("-date")
    serializer_class = ElectionSerializer
    permission_classes = [permissions.AllowAny]

class BallotViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows elections to be viewed or edited.
    """

    lookup_field = "id"
    lookup_value_regex = "[a-z0-9.\-_]+"
    queryset = Ballot.objects.all().order_by("-date")
    serializer_class = BallotSerializer
    permission_classes = [permissions.AllowAny]

class CandidateViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    queryset = Candidate.objects.all().order_by("name")
    serializer_class = CandidateSerializer
    permission_classes = [permissions.AllowAny]


class StageViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    queryset = Stage.objects.all().order_by("-created")
    serializer_class = StageSerializer
    permission_classes = [permissions.AllowAny]


### Entity List Views


class ElectionListView(ListView):
    model = Election
    template_name = "table_view.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Elections"
        return context

class BallotListView(ListView):
    model = Ballot
    template_name = "table_view.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Ballots"
        return context

class CandidateListView(ListView):
    model = Candidate
    template_name = "table_view.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Candidates"
        return context


### Entity Detail Views


class ElectionDetailView(DetailView):
    model = Election
    template_name = "election_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["ballots"] = Ballot.objects.filter(parent=self.object)
        return context

class BallotDetailView(DetailView):
    model = Ballot
    template_name = "ballot_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["stages"] = Stage.objects.filter(ballot=self.object)
        return context


class CandidateDetailView(DetailView):
    model = Candidate
    template_name = "candidate_detail.html"


class StageDetailView(DetailView):
    model = Stage
    template_name = "stage_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["stagecells"] = StageCell.objects.filter(stage=self.object)
        return context
