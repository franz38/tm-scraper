from typing import List
from cache.client import Client 
from utils.get_box import get_box


class CompetitionData:
    def __init__(self, id: str, name: str=None, 
                 number_of_teams=None, 
                 number_of_players=None, 
                 foreigners=None, 
                 avg_mv=None, 
                 avg_age=None, 
                 mvp=None,
                 clubs: List[str]=None):
        self.id = id
        self.name = name
        self.number_of_teams = number_of_teams
        self.number_of_players = number_of_players
        self.foreigners = foreigners
        self.avg_mv = avg_mv
        self.avg_age = avg_age
        self.mvp = mvp
        self.clubs = clubs


class CompetitionInstance:
    id: str
    _data: CompetitionData


    def __init__(self, id: str):
        self.id = id
        self._data = None


    def _scrape(self, season: str = None):
        url = "https://www.transfermarkt.com" + self.id + ("?saison_id=" + season if season else "")
        soup = Client().scrape(url)

        rows = get_box(soup, "clubs").find("tbody").find_all("tr")
        clubs_id = [row.find_all("td")[1].find("a")["href"] for row  in rows]

        name = soup.find(class_="data-header__headline-wrapper").get_text().strip()

        fields = soup.find_all(class_="data-header__label")
        values = [x.find(class_="data-header__content").get_text().strip().lower() for x in fields]

        for f in fields:
            f.find(class_="data-header__content").clear()
        keys = [x.get_text().strip().lower() for x in fields]

        cp = CompetitionData(id=self.id, name=name, clubs=clubs_id)

        for i, key in enumerate(keys):

            if "reigning champion" in key:
                pass
            elif "number of teams" in key:
                cp.number_of_teams = values[i]
            elif "players" in key:
                cp.number_of_players = values[i]
            elif "market value" in key:
                cp.avg_mv = values[i]
            elif "age" in key:
                cp.avg_age = values[i]
            elif "valuable" in key:
                cp.mvp = values[i]

        self._data = cp
    

    def get_data(self, season: str = None) -> CompetitionData:
        if not self._data:
            self._scrape(season)
        return self._data