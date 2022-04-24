from django.contrib.auth.models import User, Group
from rest_framework import serializers

from .models import Election, Candidate, Stage


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["url", "username", "email", "groups"]


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ["url", "name"]


class ElectionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Election
        # Removing the 'url' from below stops the ImproperlyConfigured error
        fields = ["url", "org", "date", "constituency", "parent"]
        read_only_fields = ["url"]
        depth = 1


class CandidateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Candidate
        fields = ["url", "id", "name", "party_name"]
        depth = 1


class StageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Stage
        fields = ["url", "election", "count_stage", "author"]
        depth = 1
