from spiders.search import search
from query.tables import ClubTable, PlayerTable, CompetitionTable
from utils.singleton import Singleton
from tmquery.client import Client


class TMQuery(metaclass=Singleton):

    def __init__(self, cache_results: bool = False):
        Client(cache_results=cache_results)
    

    def search_club(self, query: str) -> ClubTable:
        ids = search(query, "club")
        return ClubTable(ids)


    def search_player(self, query: str) -> PlayerTable:
        ids = search(query, "player")
        return PlayerTable(ids)


    def search_competition(self, query: str):
        ids = search(query, "competition")
        return CompetitionTable(ids)
