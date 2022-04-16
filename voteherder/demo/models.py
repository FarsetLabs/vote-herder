from django.db import models
from django.contrib.auth.models import User

from uk_election_ids import election_ids


class Election(models.Model):
    """
    System/Admin defined minimum object model to reference to the democracyclub api's for further augmentation

    Intended such that 'top level elections' are forward-forward referenced by their grouped-elections

    i.e. Election('nia.belfast-east.2022-05-05', parent=Election.get('nia.2022-05-05'))
    """

    _id = models.CharField(name='id', primary_key=True, validators = [election_ids.validate], max_length=32)
    parent = models.ForeignKey(to='self', on_delete=models.CASCADE, default=None)


class Candidate(models.Model):
    """
    System/Admin defined minimum object model to reference to the democracyclub api's for further augmentation

    Candidates can participate in any number of elections in theory...

    In practice, candidates should _not_ be able to participate twice in a given root/parent election
    """
    _id = models.IntegerField(name='id', primary_key=True)
    standing = models.ManyToManyField(Election)


class Stage(models.Model):
    """
    User-generated Stage counts wrapper; this is the primary tracking element for count tracking.
    """
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    evidence_url = models.URLField(verbose_name='Paste a link to evidence of this count stage (twitter picture/etc)')


class StageCell(models.Model):
    """
    Representation of a single candidate/stage/count entry
    """

    _id = models.UUIDField(primary_key=True)
    stage = models.ForeignKey(to=Stage, on_delete=models.CASCADE)
    candidate = models.ForeignKey(to=Candidate, on_delete=models.CASCADE)
    count = models.IntegerField()





    def __str__(self):
        return f'{self.author.username}: {self.title}'