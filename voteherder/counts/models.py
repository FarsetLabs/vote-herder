import requests
from computed_property import ComputedDateField, ComputedCharField
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models
from uk_election_ids import election_ids

from .utils import uuidv6, parse_election_id


class Election(models.Model):
    """
    System/Admin defined minimum object model to reference to the democracyclub api's for further augmentation
    """

    _id = models.CharField(
        name="id", primary_key=True, validators=[election_ids.validate], max_length=32
    )
    date = ComputedDateField(compute_from="_date")
    org = ComputedCharField(compute_from="_org", max_length=32)

    @property
    def _date(self):
        return parse_election_id(self.id)["date"]

    @property
    def _org(self):
        return parse_election_id(self.id)["org"]

    def get_data(self):
        return requests.get(
            f"https://candidates.democracyclub.org.uk/api/next/elections/{self.id}/"
        ).json()

    def build_results_json(self):
        """
        https://github.com/NICVA/electionsni/blob/master/2017/constituency/belfast-east/ResultsJson.json
        Used to power the Stages animations in here https://github.com/NICVA/electionsni/blob/master/website/js/stages.js


        When you come back to this check this out https://github.com/NICVA/electionsni/blob/master/other/mock/all-counts-create-json.py
        """
        raise NotImplementedError("#TODO")

    def populate_child_ballots(self):
        """Build all election from a "root" election"""
        data = self.get_data()
        if "ballots" in data:
            ballots = []
            for ballot in data["ballots"]:
                e, created = Ballot.objects.get_or_create(
                    id=ballot["ballot_paper_id"], election=self
                )

    def __str__(self):
        return f"{self.id}"

    class Meta:
        ordering = ["date", "org"]


class Ballot(models.Model):
    """
    System/Admin defined minimum object model to reference to the democracyclub api's for further augmentation
    """
    _id = models.CharField(
        name="id", primary_key=True, validators=[election_ids.validate], max_length=32
    )
    date = ComputedDateField(compute_from="_date")
    org = ComputedCharField(compute_from="_org", max_length=32)

    constituency = ComputedCharField(
        compute_from="_constituency", max_length=32, null=True
    )
    election = models.ForeignKey(
        to=Election, on_delete=models.CASCADE, default=None, null=True
    )
    @property
    def _date(self):
        return parse_election_id(self.id)["date"]

    @property
    def _org(self):
        return parse_election_id(self.id)["org"]

    @property
    def _constituency(self):
        return parse_election_id(self.id).get("constituency", None)

    def get_data(self):
        return requests.get(
            f"https://candidates.democracyclub.org.uk/api/next/ballots/{self.id}/"
        ).json()

    def populate_candidates(self):
        """Build / Update all candidates standing in this election"""
        data = self.get_data()
        for candidate in data["candidacies"]:
            ## Candidates may change affiliations or names between elections
            # So get solely on the id first, then do a create
            # Need to do this if we're _adding_ standings rather than bulk_create
            if Candidate.objects.filter(id=candidate["person"]["id"]).exists():
                c = Candidate.objects.get(id=candidate["person"]["id"])
            else:
                c = Candidate.objects.create(
                    id=candidate["person"]["id"],
                    name=candidate["person"]["name"],
                    party_id=candidate["party"]["ec_id"],
                    party_name=candidate["party"]["name"],
                )
            c.standing.add(self)
            c.save()

    class Meta:
        ordering = ["date", "org", "constituency"]

class Candidate(models.Model):
    """
    System/Admin defined minimum object model to reference to the democracyclub api's for further augmentation

    Candidates can participate in any number of elections in theory...

    In practice, candidates should _not_ be able to participate twice in a given root/parent election
    """

    _id = models.IntegerField(name="id", primary_key=True)
    name = models.CharField(max_length=32)
    party_id = models.CharField(max_length=32)
    party_name = models.CharField(max_length=32)
    standing = models.ManyToManyField(Ballot)

    def get_data(self):
        return requests.get(
            f"https://candidates.democracyclub.org.uk/api/next/people/{self.id}/"
        ).json()

    def __str__(self):
        return f"{self.name} ({self.party_name})"

    class Meta:
        ordering = ["party_name", "name"]


class Stage(models.Model):
    """
    User-generated Stage counts wrapper; this is the primary tracking element for count tracking.
    """

    _id = models.UUIDField(
        primary_key=True, default=uuidv6, editable=False, unique=True
    )
    author = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="author")
    validated_by = models.ForeignKey(
        to=User,
        default=None,
        on_delete=models.SET_NULL,
        null=True,
        related_name="validated_by",
    )  # Need to validate that user is admin
    created = models.DateTimeField(auto_now_add=True)
    ballot = models.ForeignKey(to=Ballot, on_delete=models.CASCADE)
    count_stage = models.IntegerField()
    non_transferable = models.FloatField(
        default=0.0, validators=[MinValueValidator(0.0)]
    )
    evidence_url = models.URLField(
        verbose_name="Paste a link to evidence of this count stage (twitter picture/etc)",
        null=True,
    )

    def __str__(self):
        return f"{self.ballot.id}-{self.count_stage} @ {self.author}"


class StageCell(models.Model):
    """
    Representation of a single candidate/stage/count entry
    """

    _id = models.UUIDField(
        primary_key=True, default=uuidv6, editable=False, unique=True
    )
    stage = models.ForeignKey(to=Stage, on_delete=models.CASCADE)
    candidate = models.ForeignKey(to=Candidate, on_delete=models.CASCADE)
    ## Counts have to be floats for n>1 stages due to fractional transfers in STV
    count = models.FloatField(validators=[MinValueValidator(0)])

    def __str__(self):
        return f"{self.count} for {self.candidate} in {self.stage}"
