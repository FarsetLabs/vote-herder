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

## High level concepts

_Taken from [DemocracyClub](https://candidates.democracyclub.org.uk/api/docs/next/)_

Candidates are a mix of a person and a candidacy. A candidacy is the person on a ballot. Ballots have elections and
divisions (areas, currently called posts).

A person can stand in more than one election, that is, they can have many candidacies on different ballots.

Ballots make up the main structure of the data, with each ballot being grouped by elections or divisions.

Apart from the base data model, there are two other concepts in this API.

Firstly, the data will change over time, from a ballot being announced through to results being entered.