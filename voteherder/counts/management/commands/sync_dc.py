from counts.models import Election, Ballot
from django.core.management.base import BaseCommand, CommandError
from uk_election_ids.election_ids import validate


class Command(BaseCommand):
    help = "Synchronises a given election, it's child-ballots, and their candidates against the democracyclub endpoint"

    def add_arguments(self, parser):
        parser.add_argument("election_id", type=str)

    def handle(self, *args, **options):
        election_id = options["election_id"]
        if not validate(election_id):
            raise CommandError(f"Election ID {election_id} cannot be validated")

        election, created = Election.objects.get_or_create(id=election_id)
        if created:
            self.stdout.write(f"new election, {election_id} created")

        data = election.get_data()
        if "ballots" in data:
            ballots = []
            for ballot in data["ballots"]:
                e, created = Ballot.objects.get_or_create(
                    id=ballot["ballot_paper_id"], election=election
                )
                if created:
                    self.stdout.write(
                        f"new election, {e.id} created as part of {election_id}"
                    )
                e.populate_candidates()
        else:
            election.populate_candidates()
