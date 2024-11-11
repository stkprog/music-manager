import json

class Listened:
    def __init__(self, release_id, rating, thoughts) -> None:
        self.release_id = release_id
        self.rating = rating
        self.thoughts = thoughts

    def toJSON(self) -> None:
        return json.dumps(
            self,
            default=lambda o: o.__dict__,
            sort_keys=False,
            indent=4
        )