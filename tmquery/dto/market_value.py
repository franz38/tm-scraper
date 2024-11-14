from tmquery.utils import list_to_csv


class MarketValueDTO:
    def __init__(
        self, player_id: str, player_name: str, mv: str, date: str, club: str, age: str
    ):
        self.player_id = player_id
        self.player_name = player_name
        self.mv = mv
        self.date = date
        self.club = club
        self.age = age

    def __str__(self):
        return list_to_csv(
            [self.player_name, self.player_id, self.mv, self.date, self.club, self.age]
        )

    def csv_header():
        return list_to_csv(["player_name", "player_id", "mv", "date", "club", "age"])
