from bs4 import BeautifulSoup
from typing import List, Optional
from tmquery.client import Client
from tmquery.dto import TransferDTO, MarketValueDTO, CareerStatsDTO, InjuryDTO
from tmquery.utils import get_club, list_to_csv, get_box


class PlayerData:
    def __init__(
        self,
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
        outfitter: Optional[str] = None,
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
        return list_to_csv(
            [
                self.name,
                self.date_of_birth,
                self.place_of_birth,
                self.height,
                self.citizenship,
                self.position,
                self.foot,
                self.agent,
                self.current_club,
                self.joined,
                self.expires,
                self.option,
                self.outfitter,
            ]
        )

    def csv_header():
        return list_to_csv(
            [
                "name",
                "date_of_birth",
                "place_of_birth",
                "height",
                "citizenship",
                "position",
                "foot",
                "agent",
                "current_club",
                "joined",
                "expires",
                "option",
                "outfitter",
            ]
        )


class PlayerInstance:
    id: str
    _data: PlayerData
    _mv: List[MarketValueDTO]
    _transfers: List[TransferDTO]
    _career_stats: List[CareerStatsDTO]
    _injuries: List[InjuryDTO]

    def __init__(self, id: str):
        self.id = id
        self._data = None
        self._mv = []
        self._transfers = []
        self._career_stats = []
        self._injuries = []

    def _scrape(self):
        url = self.id
        soup = Client().scrape(url)

        self._data = self._scrape_player_data(soup, PlayerData(id=self.id))
        self._scrape_mv()
        self._scrape_transfers()

    def _scrape_player_data(
        self, soup: BeautifulSoup, player: PlayerData
    ) -> "PlayerData":
        if soup.find(class_="data-header__headline-wrapper").find(
            class_="data-header__shirt-number"
        ):
            soup.find(class_="data-header__headline-wrapper").find(
                class_="data-header__shirt-number"
            ).clear()
        player.name = (
            soup.find(class_="data-header__headline-wrapper").get_text().strip()
        )

        data_box = get_box(soup, "player data")
        keys: List[str] = [
            x.get_text().strip().replace("&nbsp;", " ").replace("\xa0", " ").lower()
            for x in data_box.find_all(class_="info-table__content--regular")
        ]
        values = data_box.find_all(class_="info-table__content--bold")

        for i, key in enumerate(keys):
            text = (
                values[i].get_text().strip().replace("&nbsp;", " ").replace("\xa0", " ")
            )

            if "date of birth" in key:
                player.date_of_birth = text
            elif "place of birth" in key:
                player.place_of_birth = text
            elif "height" in key.lower():
                player.height = text
            elif "citizenship" in key:
                player.citizenship = ", ".join(
                    [x["alt"] for x in values[i].find_all("img")]
                )
            elif "position" in key:
                player.position = text
            elif "foot" in key:
                player.foot = text
            elif "agent" in key:
                player.agent = (
                    values[i].find("a")["href"].strip() if values[i].find("a") else text
                )
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
        url = (
            "/ceapi/marketValueDevelopment/graph/"
            + number_id
        )
        r = Client().fetch(url)

        mvalues: List[MarketValueDTO] = []
        for val in r["list"]:
            mvalues.append(
                MarketValueDTO(
                    player_id=self.id,
                    player_name=self._data.name,
                    age=val["age"],
                    club=val["verein"],
                    date=val["datum_mw"],
                    mv=val["mw"],
                )
            )
        self._mv = mvalues

    def _scrape_transfers(self):
        number_id = self.id.split("/").pop()
        url = "/ceapi/transferHistory/list/" + number_id
        r = Client().fetch(url)

        for val in r["transfers"]:
            tr = TransferDTO(
                season=val["season"],
                date=val["date"],
                fee=val["fee"],
                mv=val["marketValue"],
                joined= val["to"]["clubName"],
                left= val["from"]["clubName"],
                player_id=self.id,
                player_name=self._data.name,
                joined_id= val["to"]["href"],
                left_id= val["from"]["href"],
            )
            self._transfers.append(tr)

    def _scrape_injuries(self):
        _id = self.id.split("/profil/spieler/")
        url = (
            _id[0]
            + "/verletzungen/spieler/"
            + _id[1]
            + "/plus/1"
        )
        soup = Client().scrape(url)
        rows = (
            get_box(soup, "injury history")
            .find("table", class_="items")
            .find("tbody")
            .find_all("tr")
        )

        injuries: List[InjuryDTO] = []
        for row in rows:
            tds = row.find_all("td")
            injury = InjuryDTO(
                season=tds[0].get_text().strip(),
                injury=tds[1].get_text().strip(),
                from_=tds[2].get_text().strip(),
                until=tds[3].get_text().strip(),
                days=tds[4].get_text().strip(),
                games_missed="",
            )
            injuries.append(injury)
        self._injuries = injuries

    def _scrape_career_stats(self):
        _id = self.id.split("/profil/spieler/")
        url = (
            _id[0]
            + "/leistungsdaten/spieler/"
            + _id[1]
            + "/plus/1?saison=ges"
        )
        soup = Client().scrape(url)
        rows = (
            get_box(soup, "career stats")
            .find("table", class_="items")
            .find("tbody")
            .find_all("tr")
        )

        def parse(x):
            text = x.get_text().strip()
            if text.isnumeric():
                return int(text)
            return None

        stats: List[CareerStatsDTO] = []
        for row in rows:
            tds = row.find_all("td")
            stat = CareerStatsDTO(
                player_id=self.id,
                competition=tds[1].find("a").get_text().strip(),
                appearences=tds[2].find("a").get_text().strip(),
                competition_id=tds[1].find("a")["href"],
                goals=parse(tds[3]),
                assists=parse(tds[4]),
                og=parse(tds[5]),
                sub_on=parse(tds[6]),
                sub_off=parse(tds[7]),
                yellow_cards=parse(tds[8]),
                double_yellow=parse(tds[9]),
                red_cards=parse(tds[10]),
                penalty_goals=parse(tds[11]),
                minutes_per_goal=tds[12].get_text().strip(),
                minutes_played=tds[13].get_text().strip(),
            )
            stats.append(stat)

        self._career_stats = stats

    def get_data(self) -> PlayerData:
        if not self._data:
            self._scrape()
        return self._data

    def get_market_value(self) -> List[MarketValueDTO]:
        if not self._mv:
            self._scrape()
        return self._mv

    def get_transfers(self) -> List[TransferDTO]:
        if not self._transfers:
            self._scrape()
        return self._transfers

    def get_careeer_stats(self) -> List[CareerStatsDTO]:
        if not self._career_stats:
            self._scrape_career_stats()
        return self._career_stats

    def get_injuries(self) -> List[InjuryDTO]:
        if not self._injuries:
            self._scrape_injuries()
        return self._injuries
    
    def get_club(self, season: str = None) -> str:
        self.get_transfers()
        club_id = get_club(self._transfers, season).replace("transfers", "startseite")
        return club_id
