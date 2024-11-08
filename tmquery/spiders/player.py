from bs4 import BeautifulSoup
from tmquery.client import Client
from utils.get_box import get_box
from typing import List, Optional
from utils.list_to_csv import list_to_csv

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
        return list_to_csv([self.player_name, self.mv, self.date, 
                            self.club, self.age, self.player_id])

    def csv_header():
        return list_to_csv(["name", "mv", "date", 
                            "club", "age", "id"])


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
        return list_to_csv([self.player_name, self.season, self.date, self.left, 
                            self.joined, self.mv, self.fee, self.player_id])

    def csv_header():
        return list_to_csv(["player", "season", "date", "left", 
                            "joined", "mv", "fee", "player_id"])



class PlayerInstance:
    id: str
    _data: PlayerData
    _mv: List[MarketValue]
    _transfers: List[Transfer]


    def __init__(self, id: str):
        self.id = id
        self._data = None
        self._mv = []
        self._transfers = []
    

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