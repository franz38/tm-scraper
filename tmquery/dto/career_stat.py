from typing import Optional
from tmquery.utils import list_to_csv


class CareerStatsDTO:
    def __init__(
        self,
        player_id: str,
        competition: Optional[str] = None,
        competition_id: Optional[str] = None,
        appearences: Optional[int] = None,
        goals: Optional[int] = None,
        assists: Optional[int] = None,
        og: Optional[int] = None,
        sub_on: Optional[int] = None,
        sub_off: Optional[int] = None,
        yellow_cards: Optional[int] = None,
        double_yellow: Optional[int] = None,
        red_cards: Optional[int] = None,
        penalty_goals: Optional[int] = None,
        minutes_per_goal: Optional[str] = None,
        minutes_played: Optional[str] = None,
    ):
        self.player_id = player_id
        self.competition = competition
        self.competition_id = competition_id
        self.appearences = appearences
        self.goals = goals
        self.assists = assists
        self.og = og
        self.sub_on = sub_on
        self.sub_off = sub_off
        self.yellow_cards = yellow_cards
        self.double_yellow = double_yellow
        self.red_cards = red_cards
        self.penalty_goals = penalty_goals
        self.minutes_per_goal = minutes_per_goal
        self.minutes_played = minutes_played

    def __str__(self):
        return list_to_csv(
            [
                self.player_id,
                self.competition,
                self.competition_id,
                self.appearences,
                self.goals,
                self.assists,
                self.og,
                self.sub_on,
                self.sub_off,
                self.yellow_cards,
                self.double_yellow,
                self.red_cards,
                self.penalty_goals,
                self.minutes_per_goal,
                self.minutes_played,
            ]
        )

    def csv_header():
        return list_to_csv(
            [
                "player_id",
                "competition",
                "competition_id",
                "appearences",
                "goals",
                "assists",
                "og",
                "sub_on",
                "sub_off",
                "yellow_cards",
                "double_yellow",
                "red_cards",
                "penalty_goals",
                "minutes_per_goal",
                "minutes_played",
            ]
        )
