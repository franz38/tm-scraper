from tmquery.query.query import TMQuery


def test_get_data():
    
    competition_data = TMQuery(cache_results=True).search_competition("premier league").get_data()[0]
    
    assert competition_data.name == "Premier League"
    assert competition_data.id == "/premier-league/startseite/wettbewerb/GB1"