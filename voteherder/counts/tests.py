import difflib

import requests_cache
from django.contrib.auth.models import User
from django.test import TestCase

from .models import Election, Candidate, Stage, StageCell
from .utils import parse_election_id, get_elections_ni_constituency_count_data

# Create your tests here.

requests_cache.install_cache(expire_after=3600, allowable_methods=("GET",))


def is_close_enough(a, b, limit=0.85):
    return difflib.SequenceMatcher(a=a, b=b).ratio() > limit


class BasicElectionTestCase(TestCase):
    def setUp(self) -> None:
        Election.objects.create(id="nia.2022-05-05")

    def test_can_lookup_election_data(self):
        """Test can lookup hopefully valid election data via democracyclub"""
        election = Election.objects.get(id="nia.2022-05-05")
        election_data = election.get_data()
        self.assertEqual(election_data["slug"], "nia.2022-05-05")

    def test_can_populate_election_data(self):
        """Test can lookup valid election data via democracy club
        and subsequently populate all child elections (ballots)"""
        election = Election.objects.get(id="nia.2022-05-05")
        election_data = election.get_data()
        ballots = []

        for ballot in election_data["ballots"]:
            ballots.append(Election(id=ballot["ballot_paper_id"], parent=election))

        Election.objects.bulk_create(ballots)

        example_ballot = Election.objects.last()
        self.assertEqual(example_ballot.parent, election)


class BasicCandidateTestCases(TestCase):
    def setUp(self) -> None:
        Election.objects.get_or_create(
            id="nia.belfast-east.2022-05-05",
            parent=Election.objects.create(id="nia.2022-05-05"),
        )

    def test_can_populate_candidate_data_on_one_ballot(self):
        ballot, _ = Election.objects.get_or_create(id="nia.belfast-east.2022-05-05")
        self.assertIsNotNone(ballot.parent)
        ballot_data = ballot.get_data()

        for candidate in ballot_data["candidacies"]:
            # Need to do this if we're _adding_ standings rather than bulk_create
            c, created = Candidate.objects.get_or_create(
                id=candidate["person"]["id"],
                name=candidate["person"]["name"],
                party_id=candidate["party"]["ec_id"],
                party_name=candidate["party"]["name"],
            )
            c.standing.add(ballot)
            c.save()
        candidate_count = 0
        for candidate in Candidate.objects.all():
            self.assertTrue(candidate.standing.contains(ballot))
            candidate_count += 1
        self.assertGreater(candidate_count, 1)

    def test_can_populate_candidate_data_on_one_ballot_internal(self):
        ballot, _ = Election.objects.get_or_create(id="nia.belfast-east.2022-05-05")
        ballot.populate_candidates()
        candidate_count = 0
        for candidate in Candidate.objects.all():
            self.assertTrue(candidate.standing.contains(ballot))
            candidate_count += 1
        self.assertGreater(candidate_count, 1)


class RetroactiveCountStageParsing(TestCase):
    """Pull data in from ElectionsNI data set located at
    https://github.com/NICVA/electionsni/tree/master/2017/constituency/belfast-east"""

    ELECTION_ID = "nia.belfast-east.2017-03-02"
    ROOT_ELECTION_ID = "nia.2017-03-02"

    def setUp(self) -> None:
        self._author, _ = User.objects.get_or_create(
            username="test_user", password="test_pass", is_staff=False
        )
        ballot, _ = Election.objects.get_or_create(
            id=self.ELECTION_ID,
            parent=Election.objects.create(id=self.ROOT_ELECTION_ID),
        )
        ballot.populate_candidates()

    def test_can_populate_stages_from_electionsni(self):
        ballot = Election.objects.get(id=self.ELECTION_ID)
        ballot_desc = parse_election_id(self.ELECTION_ID)
        count_data = get_elections_ni_constituency_count_data(
            year=ballot_desc["date"].year, constituency=ballot_desc["constituency"]
        )
        stage = None
        stage_number = 0
        stage_cells = []
        counted_stages = []
        for count_row in count_data:
            if (new_stage := int(count_row["Count_Number"])) != stage_number:
                counted_stages.append(stage_number)  # for testing monotonicity later
                stage_number = new_stage
                stage = Stage.objects.create(
                    count_stage=new_stage, election=ballot, author=self._author
                )
            candidate = Candidate.objects.get(id=int(count_row["Candidate_Id"]))
            # This assumption is broken because the 'Conservative and Unionist Party' changed their names a few times
            # self.assertEqual(candidate.party_name, count_row['Party_Name'])
            self.assert_(
                is_close_enough(
                    candidate.name,
                    " ".join([count_row["Firstname"], count_row["Surname"]]),
                )
            )
            count = float(count_row["Total_Votes"])

            StageCell.objects.create(stage=stage, candidate=candidate, count=count)

        self.assertSequenceEqual(counted_stages, sorted(counted_stages))

    def tearDown(self) -> None:
        self._author.delete()
