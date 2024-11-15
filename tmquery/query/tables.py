from typing import List
from tmquery.dto.injury import InjuryDTO
from tmquery.spiders import (
    ClubData,
    ClubInstance,
    PlayerData,
    PlayerInstance,
    CompetitionData,
    CompetitionInstance,
    MarketValueDTO,
    TransferDTO,
    GoalScorer,
    CareerStatsDTO,
)


class PlayerTable:
    _data: List[PlayerInstance]

    def __init__(self, ids: List[str]):
        self._data = [PlayerInstance(id) for id in ids]

    def get_club(self, season: str = None) -> "ClubTable":
        ids = [x.get_club(season) for x in self._data]
        return ClubTable(ids)

    def market_value(self) -> "List[MarketValueDTO]":
        return [value for player in self._data for value in player.get_market_value()]

    def market_value_csv(self) -> str:
        tmp_data = "\n".join(str(x) for x in self.market_value())
        return MarketValueDTO.csv_header() + "\n" + tmp_data

    def data(self, season: str = None) -> "List[PlayerData]":
        return [player.get_data() for player in self._data]

    def data_csv(self, season: str = None) -> str:
        tmp = "\n".join([str(x) for x in self.data(season)])
        return PlayerData.csv_header() + "\n" + tmp

    def transfers(self) -> "List[TransferDTO]":
        return [value for player in self._data for value in player.get_transfers()]

    def transfers_csv(self) -> str:
        tmp = "\n".join([str(x) for x in self.transfers()])
        return TransferDTO.csv_header() + "\n" + tmp

    def count(self) -> int:
        return len(self._data)

    def stats(self) -> List[CareerStatsDTO]:
        return [value for player in self._data for value in player.get_careeer_stats()]

    def stats_csv(self) -> str:
        tmp = "\n".join([str(x) for x in self.stats()])
        return CareerStatsDTO.csv_header() + "\n" + tmp

    def injuries(self) -> List[InjuryDTO]:
        return [value for player in self._data for value in player.get_injuries()]

    def injuries_csv(self) -> str:
        tmp = "\n".join([str(x) for x in self.injuries()])
        return InjuryDTO.csv_header() + "\n" + tmp


class ClubTable:
    _data: List[ClubInstance]

    def __init__(self, ids: List[str]):
        self._data = [ClubInstance(id) for id in ids]
        # print("table created", ids)

    def get_players(self, season: str = None) -> "PlayerTable":
        player_ids = [
            player_id
            for club in self._data
            for player_id in club.get_data(season).players
        ]
        return PlayerTable(player_ids)

    def data(self, season: str = None) -> "List[ClubData]":
        return [club.get_data(season) for club in self._data]

    def data_csv(self, season: str = None) -> str:
        tmp_data = "\n".join([str(x) for x in self.data(season)])
        return ClubData.csv_header() + "\n" + tmp_data

    def count(self) -> int:
        return len(self._data)


class CompetitionTable:
    _data: List[CompetitionInstance]

    def __init__(self, ids: List[str]):
        self._data = [CompetitionInstance(id) for id in ids]
        # print("table created", ids)

    def data(self, season: str = None) -> "List[CompetitionData]":
        return [competition.get_data(season) for competition in self._data]

    def data_csv(self, season: str = None) -> str:
        tmp_data = "\n".join([str(x) for x in self.data(season)])
        return CompetitionData.csv_header() + "\n" + tmp_data

    def get_clubs(self, season: str = None) -> "ClubTable":
        club_ids = [
            club_id for club in self._data for club_id in club.get_data(season).clubs
        ]
        return ClubTable(club_ids)

    def goal_scorers(self, season: str = None):
        return [
            gs
            for competition in self._data
            for gs in competition.get_goal_scorers(season)
        ]

    def goal_scorers_csv(self, season: str = None):
        tmp_data = "\n".join([str(x) for x in self.goal_scorers(season)])
        return GoalScorer.csv_header() + "\n" + tmp_data


# class MatchTable():
#     pass
