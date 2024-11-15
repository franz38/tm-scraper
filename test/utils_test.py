from tmquery.utils import get_club
from tmquery.dto import TransferDTO
import copy

def test_get_club():
    t = TransferDTO(
        date= "",
        left= "",
        joined= "",
        fee= "",
        mv="",
        joined_id="",
        left_id="",
        player_id="",
        player_name="",
        season=""
    )

    c1: TransferDTO = copy.deepcopy(t)
    c1.date = "Jul 20, 2022"
    c1.left_id = "Juventus"
    c1.joined_id = "AS Roma"

    c2: TransferDTO = copy.deepcopy(t)
    c2.date = "Jul 1, 2015"
    c2.left_id = "US Palermo"
    c2.joined_id = "Juventus"

    c3: TransferDTO = copy.deepcopy(t)
    c3.date = "Jul 20, 2012"
    c3.left_id = "Instituto ACC"
    c3.joined_id = "US Palermo"

    assert get_club([c1,c2,c3]) == "AS Roma"
    assert get_club([c1,c2,c3], "2022/2023") == "AS Roma"
    assert get_club([c1,c2,c3], "2018/2019") == "Juventus"
    assert get_club([c1,c2,c3], "2014/2015") == "Juventus"
    assert get_club([c1,c2,c3], "2000/2001") == "Instituto ACC"