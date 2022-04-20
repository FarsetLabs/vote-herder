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
        fields = ["url", "id", "org", "date", "constituency", "parent"]
        extra_kwargs = {
            'url': {'view_name': 'counts:election-detail', 'lookup_field': 'id'},
            'parent': {'view_name': 'counts:election-detail', 'lookup_field': 'id'},
        }


class CandidateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Candidate
        fields = ["url", "id", "name", "party_name"]
        extra_kwargs = {
            'url': {'view_name': 'counts:candidate-detail', 'lookup_field': 'pk'}
        }

class StageSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.UUIDField(format='hex_verbose', source='_id')

    class Meta:
        model = Stage
        fields = ["url", "id", "election", "count_stage", "author"]
        extra_kwargs = {
            'url': {'view_name': 'counts:stage-detail', 'lookup_field': '_id'},
            'election': {'view_name': 'counts:election-detail', 'lookup_field': 'id'},
            'author': {'view_name': 'counts:user-detail', 'lookup_field': 'pk'},
        }