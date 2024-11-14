from tmquery.utils import list_to_csv


class InjuryDTO:
    def __init__(
        self,
        season: str = None,
        injury: str = None,
        from_: str = None,
        until: str = None,
        days: int = 0,
        games_missed: str = None,
    ):
        self.season = season
        self.injury = injury
        self.from_ = from_
        self.until = until
        self.days = days
        self.games_missed = games_missed

    def __str__(self):
        return list_to_csv(
            [
                self.season,
                self.injury,
                self.from_,
                self.until,
                self.days,
                self.games_missed,
            ]
        )

    def csv_header():
        return list_to_csv(
            ["season", "injury", "from", "until", "days", "games_missed"]
        )
