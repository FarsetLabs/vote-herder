from django.core.management.base import BaseCommand, CommandError
from uk_election_ids.election_ids import validate

from ..models import Election


class Command(BaseCommand):
    help = "This Command Automatically drops common stages"

    def add_arguments(self, parser):
        parser.add_argument("election_id", type=str)

    def handle(self, *args, **options):
        election_id = options["election_id"]
        if not validate(election_id):
            raise CommandError(f"Election ID {election_id} cannot be validated")
        election = Election.get(id=election_id)
