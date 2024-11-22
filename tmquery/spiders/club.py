from typing import List
from tmquery.client import Client
from tmquery.dto import MatchDTO
from tmquery.utils import list_to_csv, remove_season, get_box


class ClubData:
    def __init__(self, id:str, name: str, squad_size: int, avg_age: float, 
                 foreigners: int, nt_players: int, stadium: str, current_tr: str, 
                 current_league: str, league_lvl: str, table_position: int, players: List[str]):
        self.id = id
        self.name = name
        self.squad_size = squad_size
        self.avg_age = avg_age
        self.foreigners = foreigners
        self.nt_players = nt_players
        self.stadium = stadium
        self.current_tr = current_tr
        self.players = players
        self.current_league = current_league
        self.league_lvl = league_lvl
        self.table_position = table_position
    
    def __str__(self):
        return list_to_csv([self.name, self.squad_size, self.avg_age, self.foreigners,
                            self.nt_players, self.stadium, self.current_tr])

    def csv_header():
        return list_to_csv(["name", "squad_size", "avg_age", "foreigners", 
                            "nt_players", "stadium", "current_tr"])


class ClubInstance:
    id: str
    _data: ClubData

    def __init__(self, id: str):
        self.id = id
        self._data = None
    

    def _scrape(self, season: str = None):

        _id = self.id
        if season:
            _id = remove_season(_id)

        url = _id + ("?saison_id=" + season if season is not None else "")

        soup = Client().scrape(url)
        squadBox = get_box(soup, "squad")

        players = []
        for row in squadBox.find("table", class_="items").find("tbody").find_all("tr", recursive=False):
            player_id = row.find("td", class_="hauptlink").find("a")["href"]
            players.append(player_id)
        
        if soup.find(class_="data-header__headline-wrapper").find(class_="data-header__shirt-number"):
            soup.find(class_="data-header__headline-wrapper").find(class_="data-header__shirt-number").clear()
        name = soup.find(class_="data-header__headline-wrapper").get_text().strip()
            
        info = soup.find_all(class_="data-header__content")

        if len(info) == 9:
            table_position = int(info[1].find("a").get_text().strip())
        else:
            table_position = None
        
        self._data = ClubData(id=_id,
                              name= name, 
                              current_league= soup.find(class_="data-header__club").find("a").get_text().strip(),
                              league_lvl= info[0].find("a")["href"],
                              table_position= table_position,
                              squad_size= int(info[-6].get_text().strip()), 
                              avg_age=float(info[-5].get_text().strip()),
                              foreigners=int(info[-4].find("a").get_text().strip()),
                              nt_players=int(info[-3].find("a").get_text().strip()),
                              stadium=info[-2].find("a")["href"],
                              current_tr=info[-1].get_text().strip(),
                              players=players
                            )
        
        if soup.find(class_="data-header__headline-wrapper").find(class_="data-header__shirt-number"):
            soup.find(class_="data-header__headline-wrapper").find(class_="data-header__shirt-number").clear()
        self._data.name = soup.find(class_="data-header__headline-wrapper").get_text().strip()

    
    def get_competition_id(self, season: str = None) -> List[str]:
        matches = self.get_matches(season=season)
        return list(set([x.competition_id for x in matches]))


    def get_matches(self, season: str = None, competition: str = None) -> List[MatchDTO]:
        _id = self.id.split("/startseite/verein/")
        url = _id[0]  + "/spielplandatum/verein/" + _id[1] + "/plus/1?saison_id=2024"
        soup = Client().scrape(url)
        rows = get_box(soup, "fixtures by date").find(class_="responsive-table").find("tbody").find_all("tr")

        _matches: List[MatchDTO] = []
        current_competition = ""
        current_competition_id = ""
        for row in rows:
            tds = row.find_all("td")

            if len(tds) == 1:
                current_competition = tds[0].find("a").get_text()
                current_competition_id = tds[0].find("a")["href"]
            else:
                _match = MatchDTO(
                    match_day= tds[0].get_text().strip(),
                    date= tds[1].get_text().strip(),
                    time= tds[2].get_text().strip(),
                    home_team= tds[4].find("a").get_text().strip(),
                    home_team_id= tds[4].find("a")["href"].replace("spielplan", "startseite"),
                    away_team= tds[6].find("a").get_text().strip(),
                    away_team_id= tds[6].find("a")["href"].replace("spielplan", "startseite"),
                    system= tds[7].get_text().strip(),
                    coach= tds[8].get_text().strip(),
                    coach_id= tds[8].find("a")["href"] if tds[8].find("a") else "",
                    attendance= tds[9].get_text().strip(),
                    result= tds[10].get_text().strip(),
                    competition= current_competition,
                    competition_id= current_competition_id
                )
                _matches.append(_match)
        
        return _matches
    

    def get_data(self, season: str = None) -> ClubData:
        if not self._data:
            self._scrape(season)
        return self._data

