# vote-herder
Slightly Easier than Herding Cats.

## Registered Domains

* voteherder.com
* voteherder.org

## Potential Datasources

* Elections (https://elections.democracyclub.org.uk/elections/nia.2022-05-05/)
  * Includes geojson bounds https://elections.democracyclub.org.uk/elections/nia.belfast-east.2022-05-05/
* Also Candidates Data (https://candidates.democracyclub.org.uk/elections/nia.2022-05-05/)
  * Linked from Elections data too

## Getting started

### Previous Northern Ireland Elections covered by [ElectionsNI](http://www.electionsni.org/data/)

A management command is provided for importing existing election data into the data set.

This pulls in Election and Candidate data from elections.democracyclub.org.uk, and tries to match these with the Stage
count data. There are currently two 'matching' heuristics in place for 'historical' election matching;

* Scan the DemocracyClub sourced list of Candidates for a given election/ballot and take the candidate who's name has
  the highest `SequenceMatcher` ratio (as long as it's > 0.5)
* Somehow, if that's not enough, check with DemocracyClub if the presented Candidate_ID has been rolled up/deduplicated

** THIS WILL DROP ALL BALLOTS/STAGE/STAGECELL DATA FOR THE SPECIFIED CONTEST **

`python manage.py populate_nia_count nia.2017-03-02`

For a lazy copy-paste job, here you go;

```
python manage.py populate_nia_count nia.2017-03-02
python manage.py populate_nia_count nia.2016-05-05
```

**2011 doesn't exist, see [here](https://twitter.com/Bolster/status/1516117518984826881)**

## High level concepts

_Taken from [DemocracyClub](https://candidates.democracyclub.org.uk/api/docs/next/)_

Candidates are a mix of a person and a candidacy. A candidacy is the person on a ballot. Ballots have elections and
divisions (areas, currently called posts).

A person can stand in more than one election, that is, they can have many candidacies on different ballots.

Ballots make up the main structure of the data, with each ballot being grouped by elections or divisions.

Apart from the base data model, there are two other concepts in this API.

Firstly, the data will change over time, from a ballot being announced through to results being entered.