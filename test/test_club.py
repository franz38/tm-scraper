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

    players_data = TMQuery(cache_results=True).search_club("benfica").get_players().data()
    
    assert players_data[0].place_of_birth == "Donetsk"


def test_get_previous_players():

    players_data = TMQuery(cache_results=True).search_club("benfica").get_players("2015").data()
    
    assert players_data[0].id == "/ederson/profil/spieler/238223"
    assert players_data[1].id == "/julio-cesar/profil/spieler/22412"
    assert players_data[2].id == "/paulo-lopes/profil/spieler/25236"


def test_csv():

    csv = TMQuery(cache_results=True).search_club("benfica").csv()

    assert csv.split("\n")[0] == "name, squad_size, avg_age, foreigners, nt_players, stadium, current_tr"
    assert csv.split("\n")[1] == "SL Benfica, 26, 25.2, 19, 15, /benfica-lissabon/stadion/verein/294, +€86.42m"