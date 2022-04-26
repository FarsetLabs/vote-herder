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


class BallotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ballot
        # Removing the 'url' from below stops the ImproperlyConfigured error
        fields = ["id","date", "org", "constituency", "election"]
        read_only_fields = ["url"]
        depth = 2

class ElectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Election
        # Removing the 'url' from below stops the ImproperlyConfigured error
        fields = ["id","date", "org", "ballot_set"]
        depth = 1

class CandidateSerializer(serializers.ModelSerializer):
    democracy_club_url = serializers.ReadOnlyField()
    class Meta:
        model = Candidate
        fields = ["id", "name", "party_name","democracy_club_url"]

class StageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Stage
        fields = ["ballot", "count_stage", "author", "stagecell_set"]

class StageCellSerializer(serializers.ModelSerializer):
    class Meta:
        model = StageCell
        fields = ["candidate_id","count"]