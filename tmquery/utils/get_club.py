from typing import List
from tmquery.dto import TransferDTO
import datetime

def seson_2_date(season: str) -> str:
    year = int(season.split('/')[1])
    return f"Oct 01, {year}"


def get_club(transfers: List[TransferDTO], season: str = None) -> str:

    if not season:
        return transfers[0].joined_id
    
    date = seson_2_date(season)
    _date = datetime.datetime.strptime(date, "%b %d, %Y").date()

    for t in transfers:
        _d = datetime.datetime.strptime(t.date, "%b %d, %Y").date()
        if _d < _date:
            return t.joined_id
        
    return transfers[-1].left_id