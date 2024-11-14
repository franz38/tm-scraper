from bs4 import BeautifulSoup
from typing import List, Optional
from tmquery.client import Client
from tmquery.utils import list_to_csv, get_box


class PlayerData:
    def __init__(self,
                 id: str,
                 name: Optional[str] = None,
                 date_of_birth: Optional[str] = None,
                 place_of_birth: Optional[str] = None,
                 height: Optional[str] = None,
                 citizenship: Optional[str] = None,
                 position: Optional[str] = None,
                 foot: Optional[str] = None,
                 agent: Optional[str] = None,
                 current_club: Optional[str] = None,
                 joined: Optional[str] = None,
                 expires: Optional[str] = None,
                 option: Optional[str] = None,
                 outfitter: Optional[str] = None
                 ):
        self.id = id
        self.name = name
        self.date_of_birth = date_of_birth
        self.place_of_birth = place_of_birth
        self.height = height
        self.citizenship = citizenship
        self.position = position
        self.foot = foot
        self.agent = agent
        self.current_club = current_club
        self.joined = joined
        self.expires = expires
        self.option = option
        self.outfitter = outfitter

    def __str__(self):
        return list_to_csv([self.name, self.date_of_birth, self.place_of_birth, self.height, 
                            self.citizenship, self.position, self.foot, self.agent,
                            self.current_club, self.joined, self.expires, self.option, self.outfitter])

    
    def csv_header():
        return list_to_csv(["name", "date_of_birth", "place_of_birth", 
                            "height", "citizenship", "position", "foot",
                            "agent", "current_club", "joined", "expires", 
                            "option", "outfitter"])


class MarketValue:

    def __init__(self, player_id: str, player_name: str, mv: str, date: str, club: str, age: str):
        self.player_id = player_id
        self.player_name = player_name
        self.mv = mv
        self.date = date
        self.club = club
        self.age = age

    def __str__(self):
        return list_to_csv([self.player_name, self.player_id, self.mv, 
                            self.date, self.club, self.age])

    def csv_header():
        return list_to_csv(["player_name", "player_id",  "mv", 
                            "date", "club", "age"])


class Transfer:

    def __init__(self, player_name: str, season: str, date: str, left: str, joined: str, mv: str, fee: str, player_id: str):
        self.season = season
        self.date = date
        self.left = left
        self.joined = joined
        self.mv = mv
        self.fee = fee
        self.player_name = player_name
        self.player_id = player_id
    
    def __str__(self):
        return list_to_csv([self.player_name, self.player_id, self.season, self.date, self.left, 
                            self.joined, self.mv, self.fee])

    def csv_header():
        return list_to_csv(["player", "player_id", "season", "date", "left", 
                            "joined", "mv", "fee"])


class CareerStats:
    
    def __init__(self, player_id: str, competition: Optional[str] = None, competition_id: Optional[str] = None, appearences: Optional[int] = None, goals: Optional[int] = None, assists: Optional[int] = None, og: Optional[int] = None,
                 sub_on: Optional[int] = None, sub_off: Optional[int] = None, yellow_cards: Optional[int] = None, double_yellow: Optional[int] = None, red_cards: Optional[int] = None, penalty_goals: Optional[int] = None,
                 minutes_per_goal: Optional[str] = None, minutes_played: Optional[str] = None):
        self.player_id = player_id
        self.competition = competition
        self.competition_id = competition_id
        self.appearences = appearences
        self.goals = goals
        self.assists = assists
        self.og = og
        self.sub_on = sub_on
        self.sub_off = sub_off
        self.yellow_cards = yellow_cards
        self.double_yellow = double_yellow
        self.red_cards = red_cards
        self.penalty_goals = penalty_goals
        self.minutes_per_goal = minutes_per_goal
        self.minutes_played = minutes_played
    
    def __str__(self):
        return list_to_csv([self.player_id, self.competition, self.competition_id, self.appearences, self.goals, self.assists, 
                    self.og, self.sub_on, self.sub_off, self.yellow_cards, self.double_yellow, 
                    self.red_cards, self.penalty_goals, self.minutes_per_goal, self.minutes_played])

    def csv_header():
        return list_to_csv(["player_id", "competition", "competition_id", "appearences", "goals", "assists", 
         "og", "sub_on", "sub_off", "yellow_cards", "double_yellow", "red_cards", 
         "penalty_goals", "minutes_per_goal", "minutes_played"])


class PlayerInstance:
    id: str
    _data: PlayerData
    _mv: List[MarketValue]
    _transfers: List[Transfer]
    _career_stats: List[CareerStats]


    def __init__(self, id: str):
        self.id = id
        self._data = None
        self._mv = []
        self._transfers = []
        self._career_stats = []
    

    def _scrape(self):
        url = "https://www.transfermarkt.com" + self.id
        soup = Client().scrape(url)

        self._data = self._scrape_player_data(soup, PlayerData(id=self.id))
        self._scrape_mv()
        self._scrape_transfers()
        print("player scraped: " + url)
    

    def _scrape_player_data(self, soup: BeautifulSoup, player: PlayerData) -> 'PlayerData':
        
        if soup.find(class_="data-header__headline-wrapper").find(class_="data-header__shirt-number"):
            soup.find(class_="data-header__headline-wrapper").find(class_="data-header__shirt-number").clear()
        player.name = soup.find(class_="data-header__headline-wrapper").get_text().strip()

        data_box = get_box(soup, "player data")
        keys: List[str] = [x.get_text().strip().replace("&nbsp;", " ").replace(u'\xa0', u' ').lower() for x in data_box.find_all(class_="info-table__content--regular")]
        values = data_box.find_all(class_="info-table__content--bold")

        for i,key in enumerate(keys):
            text = values[i].get_text().strip().replace("&nbsp;", " ").replace(u'\xa0', u' ')

            if "date of birth" in key:
                player.date_of_birth = text
            elif "place of birth" in key:
                player.place_of_birth = text
            elif "height" in key.lower():
                player.height = text
            elif "citizenship" in key:
                player.citizenship = ", ".join([x["alt"] for x in values[i].find_all("img")])
            elif "position" in key:
                player.position = text
            elif "foot" in key:
                player.foot = text
            elif "agent" in key:
                player.agent = values[i].find("a")["href"].strip() if values[i].find("a") else text
            elif "club" in key:
                if values[i].find("a"):
                    player.current_club = values[i].find("a")["href"]
            elif "joined" in key:
                player.joined = text
            elif "expires" in key:
                player.expires = text
            elif "option" in key:
                player.option = text
            elif "outfitter" in key:
                player.outfitter = text

        return player


    def _scrape_mv(self):
        number_id = self.id.split("/").pop()
        url = "https://www.transfermarkt.com/ceapi/marketValueDevelopment/graph/" + number_id
        r = Client().fetch(url)

        mvalues: List[MarketValue] = []
        for val in r["list"]:
            mvalues.append(MarketValue(player_id=self.id, player_name=self._data.name,
                                       age=val["age"], club=val["verein"], 
                                       date=val["datum_mw"], mv=val["mw"]))
        self._mv = mvalues


    def _scrape_transfers(self):

        number_id = self.id.split("/").pop()
        url = "https://www.transfermarkt.com/ceapi/transferHistory/list/" + number_id
        r = Client().fetch(url)

        for val in r["transfers"]:
            tr = Transfer(
                season=val["season"],
                date=val["date"],
                fee=val["fee"],
                mv=val["marketValue"],
                joined=val["to"]["clubName"],
                left=val["from"]["clubName"],
                player_id=self.id,
                player_name=self._data.name
            )
            self._transfers.append(tr)
        

    def _scrape_career_stats(self):
        print(self.id)
        _id = self.id.split("/profil/spieler/")
        print(_id)
        url = "https://www.transfermarkt.com" + _id[0] + "/leistungsdaten/spieler/" + _id[1] + "/plus/1?saison=ges"
        soup = Client().scrape(url)
        rows = get_box(soup, "career stats").find("table", class_="items").find("tbody").find_all("tr")
        
        def parse(x):
            text = x.get_text().strip()
            if text.isnumeric():
                return int(text)
            return None

        stats: List[CareerStats] = []
        for row in rows:
            tds = row.find_all("td")
            stat = CareerStats(
                player_id= self.id,
                competition= tds[1].find("a").get_text().strip(),
                appearences= tds[2].find("a").get_text().strip(),
                competition_id= tds[1].find("a")["href"],
                goals= parse(tds[3]),
                assists= parse(tds[4]),
                og= parse(tds[5]),
                sub_on= parse(tds[6]),
                sub_off= parse(tds[7]),
                yellow_cards= parse(tds[8]),
                double_yellow= parse(tds[9]),
                red_cards= parse(tds[10]),
                penalty_goals= parse(tds[11]),
                minutes_per_goal= tds[12].get_text().strip(),
                minutes_played= tds[13].get_text().strip()
            )
            stats.append(stat)

        self._career_stats = stats


    def get_data(self) -> PlayerData:
        if not self._data:
            self._scrape()
        return self._data

    def get_market_value(self) -> List[MarketValue]:
        if not self._mv:
            self._scrape()
        return self._mv
    
    def get_transfers(self) -> List[Transfer]:
        if not self._transfers:
            self._scrape()
        return self._transfers
    
    def get_careeer_stats(self) -> List[CareerStats]:
        if not self._career_stats:
            self._scrape_career_stats()
        return self._career_stats