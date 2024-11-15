from tmquery.client import Client
from tmquery.utils import list_to_csv, remove_season, get_box


class ClubData:
    def __init__(self, id:str, name: str, squad_size: int, avg_age: float, 
                 foreigners: int, nt_players: int, stadium: str, current_tr: str, 
                 current_league: str, league_lvl: str, table_position: int, players: list[str]):
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
        
        self._data = ClubData(id=_id,
                              name= name, 
                              current_league= soup.find(class_="data-header__club").find("a").get_text().strip(),
                              league_lvl= info[0].find("a")["href"],
                              table_position= int(info[1].find("a").get_text().strip()),
                              squad_size= int(info[3].get_text().strip()), 
                              avg_age=float(info[4].get_text().strip()),
                              foreigners=int(info[5].find("a").get_text().strip()),
                              nt_players=int(info[6].find("a").get_text().strip()),
                              stadium=info[7].find("a")["href"],
                              current_tr=info[8].get_text().strip(),
                              players=players
                            )
        
        if soup.find(class_="data-header__headline-wrapper").find(class_="data-header__shirt-number"):
            soup.find(class_="data-header__headline-wrapper").find(class_="data-header__shirt-number").clear()
        self._data.name = soup.find(class_="data-header__headline-wrapper").get_text().strip()

        print("club scraped: " + url)

    

    def get_data(self, season: str = None) -> ClubData:
        if not self._data:
            self._scrape(season)
        return self._data

