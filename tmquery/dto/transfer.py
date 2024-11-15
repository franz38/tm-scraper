from tmquery.utils import list_to_csv


class TransferDTO:
    def __init__(
        self,
        player_name: str,
        season: str,
        date: str,
        left: str,
        joined: str,
        mv: str,
        fee: str,
        player_id: str,
        left_id: str,
        joined_id: str,
    ):
        self.season = season
        self.date = date
        self.left = left
        self.joined = joined
        self.mv = mv
        self.fee = fee
        self.player_name = player_name
        self.player_id = player_id
        self.left_id = left_id
        self.joined_id = joined_id

    def __str__(self):
        return list_to_csv(
            [
                self.player_name,
                self.player_id,
                self.season,
                self.date,
                self.left,
                self.joined,
                self.mv,
                self.fee,
            ]
        )

    def csv_header():
        return list_to_csv(
            ["player", "player_id", "season", "date", "left", "joined", "mv", "fee"]
        )
