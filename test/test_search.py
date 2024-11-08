from tmquery.query.query import TMQuery

def test_search():

    data = TMQuery(cache_results=True).search_player("di maria").get_data()[0]
    assert data.id == "/angel-di-maria/profil/spieler/45320"

    data = TMQuery(cache_results=True).search_player("milan").get_data()[0]
    assert data.id == "/milan-skriniar/profil/spieler/204069"

    data = TMQuery(cache_results=True).search_club("milan").get_data()[0]
    assert data.id == "/inter-mailand/startseite/verein/46"

    data = TMQuery(cache_results=True).search_competition("ligue 1").get_data()[0]
    assert data.id == "ligue-1/startseite/wettbewerb/FR1"
