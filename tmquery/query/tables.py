from typing import List
from spiders.club import ClubData, ClubInstance
from spiders.player import PlayerData, PlayerInstance
from spiders.competition import CompetitionData, CompetitionInstance


class PlayerTable():
    _data: List[PlayerInstance]

    def __init__(self, ids: List[str]):
        self._data = [PlayerInstance(id) for id in ids]
        print("table created", ids)

    def clubs() -> 'ClubTable':
        return ClubTable()
    
    def data(self) -> 'List[PlayerData]':
        return [player.get_data() for player in self._data]

    def count(self) -> int:
        return len(self._data)


class ClubTable():
    _data: List[ClubInstance]

    def __init__(self, ids: List[str]):
        self._data = [ClubInstance(id) for id in ids]
        print("table created", ids)
    

    def players(self, season: str = None) -> 'PlayerTable':
        player_ids = [player_id for club in self._data for player_id in club.get_data(season).players]
        return PlayerTable(player_ids)


    def data(self, season: str = None) -> 'List[ClubData]':
        return [club.get_data(season) for club in self._data]


    def count(self) -> int:
        return len(self._data)


class CompetitionTable():
    _data: List[CompetitionInstance]

    def __init__(self, ids: List[str]):
        self._data = [CompetitionInstance(id) for id in ids]
        print("table created", ids)
    

    def data(self, season: str = None) -> 'List[CompetitionData]':
        return [competition.get_data(season) for competition in self._data]
    

    def get_clubs(self, season: str = None) -> 'PlayerTable':
        club_ids = [club_id for club in self._data for club_id in club.get_data(season).clubs]
        return ClubTable(club_ids)
