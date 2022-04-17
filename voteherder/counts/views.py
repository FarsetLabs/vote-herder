# Create your views here.
from django.contrib.auth.models import User, Group
from rest_framework import permissions
from rest_framework import viewsets

from .models import Election, Candidate, Stage
from .serializers import (
    UserSerializer,
    GroupSerializer,
    ElectionSerializer,
    CandidateSerializer,
    StageSerializer,
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
    queryset = Election.objects.all().order_by("-date")
    serializer_class = ElectionSerializer
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
