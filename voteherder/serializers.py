from django.contrib.auth.models import User, Group
from rest_framework import serializers

from .models import Election, Candidate, Stage, StageCell, Ballot


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username"]


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ["name"]


class BallotSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Ballot
        fields = ["id", "url", "date", "org", "constituency", "url", "election"]
        depth = 1


class ElectionSerializer(serializers.HyperlinkedModelSerializer):
    ballot_set = BallotSerializer(many=True)

    class Meta:
        model = Election
        # Removing the 'url' from below stops the ImproperlyConfigured error
        fields = ["id", "url", "date", "org", "ballot_set"]
        depth=1


class CandidateSerializer(serializers.HyperlinkedModelSerializer):
    democracy_club_url = serializers.ReadOnlyField()

    class Meta:
        model = Candidate
        fields = ["id", "url", "name", "party_name", "democracy_club_url"]


class StageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Stage
        fields = ["ballot", "count_stage", "author", "stagecell_set"]


class StageCellSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = StageCell
        fields = ["candidate_id", "count"]
