from tmquery.query.query import TMQuery


def test_get_data():
    
    player_data = TMQuery(cache_results=True).search_player("dybala").data()[0]
    
    assert player_data.name == "Paulo Dybala"
    assert player_data.date_of_birth == "Nov 15, 1993 (30)"
    assert player_data.place_of_birth == "Laguna Larga"
    assert player_data.height == "1,77 m"
    assert player_data.citizenship == "Argentina, Italy"
    assert player_data.position == "Attack - Second Striker"
    assert player_data.foot == "left"
    assert player_data.agent == "Relatives"
    assert player_data.current_club == "/as-rom/startseite/verein/12"
    assert player_data.joined == "Jul 20, 2022"
    assert player_data.expires == "Jun 30, 2025"
    assert player_data.outfitter == "adidas"


def test_csv():

    csv = TMQuery(cache_results=True).search_player("dybala").csv()

    assert csv.split("\n")[0] == "name, date_of_birth, place_of_birth, height, citizenship, position, foot, agent, current_club, joined, expires, option, outfitter"
    assert csv.split("\n")[1] == "Paulo Dybala, Nov 15, 1993 (30), Laguna Larga, 1,77 m, Argentina, Italy, Attack - Second Striker, left, Relatives, /as-rom/startseite/verein/12, Jul 20, 2022, Jun 30, 2025, null, adidas"


def test_market_value():

    mv = TMQuery(cache_results=True).search_player("dybala").get_market_value().data()

    assert mv[0].player_id == "/paulo-dybala/profil/spieler/206050"
    assert mv[0].player_name == "Paulo Dybala"
    assert mv[0].mv == "€2.00m"
    assert mv[4].mv == "€5.00m"
    assert mv[9].mv == "€28.00m"
    assert mv[9].club == "Juventus FC"


def test_market_value_csv():

    csv = TMQuery(cache_results=True).search_player("dybala").get_market_value().csv()

    assert csv.split("\n")[0] == "player_name, player_id, mv, date, club, age"
    assert csv.split("\n")[1] == "Paulo Dybala, /paulo-dybala/profil/spieler/206050, €2.00m, Dec 23, 2011, Instituto ACC, 18"


def test_get_club():

    p = TMQuery(cache_results=True).search_player("dybala")
    
    assert p.get_club().data()[0].id == "/as-roma/startseite/verein/12/saison_id/2022"
    assert p.get_club("2023/2024").data()[0].id == "/as-roma/startseite/verein/12/saison_id/2022"
    assert p.get_club("2018/2019").data()[0].id == "/juventus/startseite/verein/506/saison_id/2015"