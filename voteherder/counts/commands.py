from models import Election, Candidate


def populate_child_ballots(election: Election):
    """Build all election from a "root" election"""
    data = election.get_data()
    if 'ballots' in data:
        ballots = []
        for ballot in data['ballots']:
            e, created = Election.objects.get_or_create(
                id=ballot['ballot_paper_id'],
                parent=election
            )


def populate_candidates(election: Election):
    """Build / Update all candidates standing in this election"""
    data = election.get_data()
    for candidate in data['candidacies']:
        # Need to do this if we're _adding_ standings rather than bulk_create
        c, created = Candidate.objects.get_or_create(
            id=candidate['person']['id'],
            name=candidate['person']['name'],
            party_id=candidate['party']['ec_id'],
            party_name=candidate['party']['name'],
        )
        c.standing.add(election)
        c.save()
