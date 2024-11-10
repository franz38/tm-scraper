from tmquery.query.query import TMQuery


def test_get_players_from_competition():
    
    # get players from serie a 2010-11 season
    players_number = TMQuery(cache_results=True).search_competition("serie a").get_clubs("2000").get_players().count()
    assert players_number == 720

    players_number = TMQuery(cache_results=True).search_competition("serie a").get_clubs("2000").get_players("2000").count()
    assert players_number == 720

    # get clubs from serie a 2000-01 and return their data
    clubs = TMQuery(cache_results=True).search_competition("serie a").get_clubs("2000").data()
    names = [c.name for c in clubs]

    assert len(clubs) == 18
    assert "AC Perugia Calcio" in names
    assert "US Lecce" in names
    assert "SS Lazio" in names
    assert "AS Roma" in names
    assert "Bologna FC 1909" in names
    assert "Udinese Calcio" in names
    assert "Brescia Calcio" in names
    assert "ACF Fiorentina" in names
    assert "Juventus FC" in names
    assert "Parma Calcio 1913" in names
    assert "Atalanta BC" in names
    assert "Hellas Verona" in names
    assert "Inter Milan" in names
    assert "Inter Milan" in names
    assert "AC Milan" in names
    assert "Reggina 1914" in names
    assert "LR Vicenza" in names
    assert "SSC Napoli" in names
    assert "SSC Bari" in names
