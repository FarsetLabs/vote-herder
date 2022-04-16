import requests
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models
from uk_election_ids import election_ids

from .utils import uuidv6


class Election(models.Model):
    """
    System/Admin defined minimum object model to reference to the democracyclub api's for further augmentation

    Intended such that 'top level elections' are forward-forward referenced by their grouped-elections

    i.e. Election('nia.belfast-east.2022-05-05', parent=Election.get('nia.2022-05-05'))
    """

    _id = models.CharField(name='id', primary_key=True, validators=[election_ids.validate], max_length=32)
    parent = models.ForeignKey(to='self', on_delete=models.CASCADE, default=None, null=True)

    def get_data(self):
        if self.parent is None:
            return requests.get(f'https://candidates.democracyclub.org.uk/api/next/elections/{self.id}/').json()
        else:
            return requests.get(f'https://candidates.democracyclub.org.uk/api/next/ballots/{self.id}/').json()

    def build_results_json(self):
        """
        https://github.com/NICVA/electionsni/blob/master/2017/constituency/belfast-east/ResultsJson.json
        Used to power the Stages animations in here https://github.com/NICVA/electionsni/blob/master/website/js/stages.js


        When you come back to this check this out https://github.com/NICVA/electionsni/blob/master/other/mock/all-counts-create-json.py
        """
        raise NotImplementedError('#TODO')

    def populate_candidates(self):
        """Build / Update all candidates standing in this election"""
        data = self.get_data()
        for candidate in data['candidacies']:
            # Need to do this if we're _adding_ standings rather than bulk_create
            c, created = Candidate.objects.get_or_create(
                id=candidate['person']['id'],
                name=candidate['person']['name'],
                party_id=candidate['party']['ec_id'],
                party_name=candidate['party']['name'],
            )
            c.standing.add(self)
            c.save()


class Candidate(models.Model):
    """
    System/Admin defined minimum object model to reference to the democracyclub api's for further augmentation

    Candidates can participate in any number of elections in theory...

    In practice, candidates should _not_ be able to participate twice in a given root/parent election
    """
    _id = models.IntegerField(name='id', primary_key=True)
    name = models.CharField(max_length=32)
    party_id = models.CharField(max_length=32)
    party_name = models.CharField(max_length=32)
    standing = models.ManyToManyField(Election)

    def get_data(self):
        return requests.get(f'https://candidates.democracyclub.org.uk/api/next/people/{self.id}/').json()


class Stage(models.Model):
    """
    User-generated Stage counts wrapper; this is the primary tracking element for count tracking.
    """
    _id = models.UUIDField(primary_key=True, default=uuidv6, editable=False, unique=True)
    author = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='author')
    validated_by = models.ForeignKey(to=User, default=None, on_delete=models.SET_NULL, null=True,
                                     related_name='validated_by')  # Need to validate that user is admin
    created = models.DateTimeField(auto_now_add=True)
    election = models.ForeignKey(to=Election, on_delete=models.CASCADE)
    count_stage = models.IntegerField()
    non_transferable = models.FloatField(
        default=0.0, validators=[MinValueValidator(0.0)]
    )
    evidence_url = models.URLField(
        verbose_name='Paste a link to evidence of this count stage (twitter picture/etc)',
        null=True
    )


class StageCell(models.Model):
    """
    Representation of a single candidate/stage/count entry
    """

    _id = models.UUIDField(primary_key=True, default=uuidv6, editable=False, unique=True)
    stage = models.ForeignKey(to=Stage, on_delete=models.CASCADE)
    candidate = models.ForeignKey(to=Candidate, on_delete=models.CASCADE)
    ## Counts have to be floats for n>1 stages due to fractional transfers in STV
    count = models.FloatField(validators=[MinValueValidator(0)])
