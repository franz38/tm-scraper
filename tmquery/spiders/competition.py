from typing import List
from tmquery.client import Client 
from utils.get_box import get_box
from utils.list_to_csv import list_to_csv

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
    
    def __str__(self):
        return list_to_csv([self.name, self.number_of_teams, self.number_of_players, self.foreigners, self.avg_mv, self.avg_age, self.mvp])

    
    def csv_header():
        return list_to_csv(["name", "number_of_teams", "number_of_players", "foreigners", "avg_mv", "avg_age", "mvp"])


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
        values = [f.find(class_="data-header__content").extract() for f in fields]
        keys = [x.get_text().strip().lower() for x in fields]

        cp = CompetitionData(id=self.id, name=name, clubs=clubs_id)

        for i, key in enumerate(keys):
            text = values[i].get_text().strip().lower()

            if "reigning champion" in key:
                pass
            elif "number of teams" in key:
                cp.number_of_teams = text
            elif "players" in key:
                cp.number_of_players = text
            elif "market value" in key:
                cp.avg_mv = text
            elif "age" in key:
                cp.avg_age = text
            elif "valuable" in key:
                cp.mvp = values[i].find("a")["href"]

        self._data = cp
    

    def get_data(self, season: str = None) -> CompetitionData:
        if not self._data:
            self._scrape(season)
        return self._data