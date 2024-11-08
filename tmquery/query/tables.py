from typing import List
from spiders.club import ClubData, ClubInstance
from spiders.player import PlayerData, PlayerInstance
from spiders.competition import CompetitionData, CompetitionInstance


class PlayerTable():
    data: List[PlayerInstance]

    def __init__(self, ids: List[str]):
        self.data = [PlayerInstance(id) for id in ids]
        print("table created", ids)

    def clubs() -> 'ClubTable':
        return ClubTable()
    
    def get_data(self) -> 'List[PlayerData]':
        return [player.get_data() for player in self.data]

    def count(self) -> int:
        return len(self.data)


class ClubTable():
    data: List[ClubInstance]

    def __init__(self, ids: List[str]):
        self.data = [ClubInstance(id) for id in ids]
        print("table created", ids)
    

    def players(self, season: str = None) -> 'PlayerTable':
        pls = [club.get_data(season).players for club in self.data]
        ids = [x for xs in pls for x in xs] # flatten array
        return PlayerTable(ids)


    def get_data(self, season: str = None) -> 'List[ClubData]':
        return [club.get_data(season) for club in self.data]


    def count(self) -> int:
        return len(self.data)


class CompetitionTable():
    data: List[CompetitionInstance]

    def __init__(self, ids: List[str]):
        self.data = [CompetitionInstance(id) for id in ids]
        print("table created", ids)
    

    def get_data(self, season: str = None) -> 'List[CompetitionData]':
        return [competition.get_data(season) for competition in self.data]
