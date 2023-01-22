import json

def create_vote_stages() -> dict:
    return dict(
        quota=150,
        constituency='East Belfast',
        stage_counts = [
            dict(
                barbara=173,
                john=123,
                sarah=45,
            ),
            dict(
                barbara=150,
                john=142,
                sarah=60,
            ),
            dict(
                barbara=150,
                john=189,
                sarah=0,
            )
        ]
    )

if __name__ == '__main__':
    votes = create_vote_stages()
    with open('votes.json', 'w') as f:
        json.dump(votes, f, indent=4)    