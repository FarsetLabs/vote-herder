# vote-herder
Slightly Easier than Herding Cats.

## Registered Domains

* electionsni.org
* voteherder.com
* voteherder.org

## Potential Datasources

* Elections (https://elections.democracyclub.org.uk/elections/nia.2022-05-05/)
  * Includes geojson bounds https://elections.democracyclub.org.uk/elections/nia.belfast-east.2022-05-05/
* Also Candidates Data (https://candidates.democracyclub.org.uk/elections/nia.2022-05-05/)
  * Linked from Elections data too

## Getting started

### Python setup
1. somehow get a python base version, pyenv can be an option
2. install python poetry
3. run `poetry install`
4. run `poetry shell` # to get your shell into the correct virtualenv

### Clean migrations

``` 
python voteherder/manage.py makemigrations counts
python voteherder/manage.py migrate    
```

### Create a local superadmin

`python voteherder/manage.py createsuperuser --username admin --email admin@voteherder.org`

### Previous Northern Ireland Elections covered by [ElectionsNI](http://www.electionsni.org/data/)

A management command is provided for importing existing election data into the data set.

This pulls in Election and Candidate data from elections.democracyclub.org.uk, and tries to match these with the Stage
count data. There are currently two 'matching' heuristics in place for 'historical' election matching;

* Scan the DemocracyClub sourced list of Candidates for a given election/ballot and take the candidate who's name has
  the highest `SequenceMatcher` ratio (as long as it's > 0.5)
* Somehow, if that's not enough, check with DemocracyClub if the presented Candidate_ID has been rolled up/deduplicated

** THIS WILL DROP ALL BALLOTS/STAGE/STAGECELL DATA FOR THE SPECIFIED CONTEST **

`python voteherder/manage.py populate_nia_count nia.2017-03-02`

For a lazy copy-paste job, here you go;

```
python voteherder/manage.py populate_nia_count nia.2017-03-02
python voteherder/manage.py populate_nia_count nia.2016-05-05
```

for a lazyer copy-paste job, here you go(or if you need to reset everything after running `rm voteherder/db.sqlite3`):

```
poetry run python voteherder/manage.py makemigrations counts
poetry run python voteherder/manage.py migrate    
poetry run python voteherder/manage.py createsuperuser --username admin --email admin@voteherder.org
poetry run python voteherder/manage.py populate_nia_count nia.2017-03-02
poetry run python voteherder/manage.py populate_nia_count nia.2016-05-05
```

**2011 doesn't exist, see [here](https://twitter.com/Bolster/status/1516117518984826881)**

### Actually running a service

```python voteherder/manage.py runserver```

Then go [here](http://127.0.0.1:8000/api/v1/elections/) to see a list of imported ballots, or [here](http://127.0.0.1:8000/swagger/) to drop into the swagger ui


## High level concepts

_Taken from [DemocracyClub](https://candidates.democracyclub.org.uk/api/docs/next/)_

Candidates are a mix of a person and a candidacy. A candidacy is the person on a ballot. Ballots have elections and
divisions (areas, currently called posts).

A person can stand in more than one election, that is, they can have many candidacies on different ballots.

Ballots make up the main structure of the data, with each ballot being grouped by elections or divisions.
