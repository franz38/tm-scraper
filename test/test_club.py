from tmquery.query.query import TMQuery


def test_get_data():

    club_data = TMQuery(cache_results=True).search_club("benfica").data()[0]

    assert club_data.squad_size == 26
    assert club_data.avg_age == 25.2
    assert club_data.foreigners == 19
    assert club_data.nt_players == 15
    assert club_data.stadium == "/benfica-lissabon/stadion/verein/294"
    assert club_data.current_tr == "+€86.42m"


def test_get_players():

    players_data = TMQuery(cache_results=True).search_club("benfica").players().data()
    
    assert players_data[0].place_of_birth == "Donetsk"