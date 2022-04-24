import codecs
import csv
import datetime
import difflib
import uuid
from contextlib import closing

import requests
from uk_election_ids import election_ids


def parse_election_id(election_id, slug=False):
    """
    >>> parse_election_id('nia.belfast-east.2022-05-05')['date'].year
    2022

    >>> parse_election_id('nia.2022-05-05')['date'].year
    2022

    >>> parse_election_id('nia_2022-05-05', slug=True)['date'].year
    2022

    """
    if slug:
        parts = election_id.split("_")
    else:
        parts = election_id.split(".")

    if len(parts) == 2:
        return {"org": parts[0], "date": datetime.date(*map(int, parts[1].split("-")))}
    elif len(parts) == 3:
        return {
            "org": parts[0],
            "constituency": parts[1],
            "date": datetime.date(*map(int, parts[2].split("-"))),
        }
    else:
        raise ValueError(f"Could not parse {election_id} as an election id slug")


def get_elections_ni_constituency_count_data(year, constituency):
    """eg http://electionsni.org/2017/constituency/belfast-east/Count.csv
    Streaming solution from https://stackoverflow.com/a/38677650/252556
    """
    url = f"http://electionsni.org/{year}/constituency/{constituency}/Count.csv"
    counts = []
    with closing(requests.get(url, stream=True)) as r:
        r.raise_for_status()
        reader = csv.DictReader(
            codecs.iterdecode(r.iter_lines(), "utf-8"), delimiter=",", quotechar='"'
        )
        for row in reader:
            counts.append(row)
    return counts


def get_alternative_person_id(candidate_id: int):
    """Sometimes people change. Maybe"""
    data = requests.get(
        f"https://candidates.democracyclub.org.uk/api/next/people/{candidate_id}/"
    ).json()

    if data["id"] != candidate_id:
        return data["id"]
    else:
        return None


def uuidv1tov6(u):
    """http://gh.peabody.io/uuidv6/"""
    uh = u.hex
    tlo1 = uh[:5]
    tlo2 = uh[5:8]
    tmid = uh[8:12]
    thig = uh[13:16]
    rest = uh[16:]
    uh6 = thig + tmid + tlo1 + "6" + tlo2 + rest
    return uuid.UUID(hex=uh6)


def uuidv6():
    return uuidv1tov6(uuid.uuid1())


def is_close_enough(a, b, limit=0.80):
    return difflib.SequenceMatcher(a=a, b=b).ratio() > limit


def terrible_validator(eid):
    """
    I HATE THIS I HATE THIS I HATE THIS
    """
    return election_ids.validate(eid.replace("_", "."))
