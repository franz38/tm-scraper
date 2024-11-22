from typing import List
from tmquery.client import Client 
from tmquery.utils import list_to_csv, get_box


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


class GoalScorer():
    def __init__(self, id: str, name: str, appearances: int, goals: int):
        self.id = id
        self.name = name
        self.appearances = appearances
        self.goals = goals
    
    def __str__(self):
        return list_to_csv([self.name, self.appearances, self.goals, self.id])

    def csv_header():
        return list_to_csv(["name", "appearances", "goals", "player_id"])


class CompetitionInstance:
    id: str
    _data: CompetitionData


    def __init__(self, id: str):
        self.id = id
        self._data = None


    def _scrape(self, season: str = None):
        url = self.id + ("?saison_id=" + season if season else "")
        soup = Client().scrape(url)

        club_box = get_box(soup, "clubs")

        if club_box:
            rows = club_box.find("tbody").find_all("tr")
            clubs_id = [row.find_all("td")[1].find("a")["href"] for row  in rows]
        else:
            details_url = url.replace("startseite", "teilnehmer")
            soup = Client().scrape(details_url)

            rows = get_box(soup, "teams").find("tbody").find_all("tr")
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
    

    def _scrape_goal_scorers(self, season: str = None) -> List[GoalScorer]:
        short_name, tier = self.id.split("/startseite/wettbewerb/")
        season_param = ("/saison_id/" + season) if season else ""
        url = short_name + "/torschuetzenliste/wettbewerb/" + tier + season_param
        soup = Client().scrape(url)

        rows = get_box(soup, "goalscorers").find("table", class_="items").find("tbody").find_all("tr", recursive=False)
        res: List[GoalScorer] = []
        for row in rows:
            tds = row.find_all("td", recursive=False)

            gs = GoalScorer(
                id= tds[1].find(class_="hauptlink").find("a")["href"],
                name= tds[1].find(class_="hauptlink").find("a").get_text().strip(),
                appearances= int(tds[5].find("a").get_text().strip()),
                goals= int(tds[6].find("a").get_text().strip())
            )
            res.append(gs)

        return res


    def get_data(self, season: str = None) -> CompetitionData:
        if not self._data:
            self._scrape(season)
        return self._data
    
    def get_goal_scorers(self, season: str = None) -> List[GoalScorer]:
        return self._scrape_goal_scorers(season)