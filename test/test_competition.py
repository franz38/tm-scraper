from tmquery.query.query import TMQuery


def test_get_data():
    
    competition_data = TMQuery(cache_results=True).search_competition("premier league").data()[0]
    
    assert competition_data.name == "Premier League"
    assert competition_data.id == "/premier-league/startseite/wettbewerb/GB1"

def test_get_players():

    clubs = TMQuery(cache_results=True).search_competition("premier league").get_clubs().data()

    assert clubs[0].id == "/manchester-city/startseite/verein/281/saison_id/2024"
    assert clubs[1].id == "/fc-arsenal/startseite/verein/11/saison_id/2024"


def test_get_previous_players():

    clubs = TMQuery(cache_results=True).search_competition("premier league").get_clubs("2017").data()

    assert clubs[0].id == "/manchester-city/startseite/verein/281/saison_id/2017"
    assert clubs[1].id == "/fc-chelsea/startseite/verein/631/saison_id/2017"