from typing import List
from tmquery.dto import InjuryDTO, MatchDTO
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

    def data(self, season: str = None) -> 'List[PlayerData]':
        return [player.get_data() for player in self._data]

    def csv(self, season: str = None) -> str:
        tmp = "\n".join([str(x) for x in self.data(season)])
        return PlayerData.csv_header() + "\n" + tmp
    
    def get_club(self, season: str = None) -> 'ClubTable':
        ids = [x.get_club(season) for x in self._data]
        return ClubTable(ids)
    
    def get_market_value(self) -> 'MarketValueTable':
        return MarketValueTable([value for player in self._data for value in player.get_market_value()])
    
    def get_transfers(self) -> 'TransferTable':
        return TransferTable([value for player in self._data for value in player.get_transfers()])

    def get_career_stats(self) -> 'CareerStatTable':
        return CareerStatTable([value for player in self._data for value in player.get_careeer_stats()])
    
    def get_injuries(self) -> 'InjuryTable':
        return InjuryTable([value for player in self._data for value in player.get_injuries()])

    def count(self) -> int:
        return len(self._data)


class ClubTable:
    _data: List[ClubInstance]

    def __init__(self, ids: List[str]):
        self._data = [ClubInstance(id) for id in ids]

    def data(self, season: str = None) -> 'List[ClubData]':
        return [club.get_data(season) for club in self._data]

    def csv(self, season: str = None) -> str:
        tmp_data = "\n".join([str(x) for x in self.data(season)])
        return ClubData.csv_header() + "\n" + tmp_data

    def get_players(self, season: str = None) -> 'PlayerTable':
        player_ids = [
            player_id
            for club in self._data
            for player_id in club.get_data(season).players
        ]
        return PlayerTable(player_ids)
    
    def get_matches(self, season: str = None) -> 'MatchTable':
        return MatchTable([match for club in self._data for match in club.get_matches(season)])
    
    def get_competitions(self, season: str = None) -> 'CompetitionTable':
        return CompetitionTable([id for club in self._data for id in club.get_competition_id(season)])
    
    def count(self) -> int:
        return len(self._data)


class CompetitionTable:
    _data: List[CompetitionInstance]

    def __init__(self, ids: List[str]):
        self._data = [CompetitionInstance(id) for id in ids]
        # print("table created", ids)

    def data(self, season: str = None) -> 'List[CompetitionData]':
        return [competition.get_data(season) for competition in self._data]

    def csv(self, season: str = None) -> str:
        tmp_data = "\n".join([str(x) for x in self.data(season)])
        return CompetitionData.csv_header() + "\n" + tmp_data

    def get_clubs(self, season: str = None) -> 'ClubTable':
        return ClubTable([club_id for club in self._data for club_id in club.get_data(season).clubs ])

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

class TransferTable:
    _data: List['TransferDTO']

    def __init__(self, data: List[TransferDTO]):
        self._data = data
    
    def data(self) -> List['TransferDTO']:
        return self._data

    def csv(self) -> str:
        return "\n".join([TransferDTO.csv_header()] + [str(x) for x in self._data])


class MarketValueTable:
    _data: List['MarketValueDTO']

    def __init__(self, data: List[MarketValueDTO]):
        self._data = data
    
    def data(self) -> List['MarketValueDTO']:
        return self._data

    def csv(self) -> str:
        return "\n".join([MarketValueDTO.csv_header()] + [str(x) for x in self._data])


class CareerStatTable:
    _data: List['CareerStatsDTO']

    def __init__(self, data: List[CareerStatsDTO]):
        self._data = data
    
    def data(self) -> List['CareerStatsDTO']:
        return self._data

    def csv(self) -> str:
        return  "\n".join([CareerStatsDTO.csv_header()] + [str(x) for x in self._data])


class InjuryTable:
    _data: List['InjuryDTO']

    def __init__(self, data: List[InjuryDTO]):
        self._data = data
    
    def data(self) -> List['InjuryDTO']:
        return self._data

    def csv(self) -> str:
        return "\n".join([InjuryDTO.csv_header()] + [str(x) for x in self._data])


class MatchTable:
    _data: List['MatchDTO']

    def __init__(self, data: List[MatchDTO]):
        self._data = data

    def data(self) -> List['MatchDTO']:
        return self._data

    def csv(self) -> str:
        return "\n".join([MatchDTO.csv_header()] + [str(x) for x in self._data])
    
    def get_away_team(self) -> ClubTable:
        return ClubTable([x.away_team_id for x in self._data])
    
    def get_home_team(self) -> ClubTable:
        return ClubTable([x.home_team_id for x in self._data])
