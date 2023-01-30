from ninja import NinjaAPI
from typing import List

from ninja import Router, ModelSchema
from .models import Ballot, Election, Stage, StageCell

# Serializers
class BallotSchema(ModelSchema):
    class Config:
        model = Ballot
        model_fields = ['id', 'date', 'constituency', 'quota', 'election']

class ElectionSchema(ModelSchema):
    class Config:
        model = Election
        model_fields = ['id', 'date']


# Routers
router = Router()

@router.get('/ballots', response=List[BallotSchema])
def list_ballots(request):
    return Ballot.objects.all()
    

@router.get('/ballot/{ballot_id}', response=BallotSchema)
def ballot_details(request, ballot_id: str):
    ballot = Ballot.objects.get(pk=ballot_id)
    return ballot
