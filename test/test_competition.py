from tmquery.query.query import TMQuery


def test_get_data():
    
    competition_data = TMQuery(cache_results=True).search_competition("premier league").data()[0]
    
    assert competition_data.name == "Premier League"
    assert competition_data.id == "/premier-league/startseite/wettbewerb/GB1"


def test_get_clubs():

    clubs = TMQuery(cache_results=True).search_competition("premier league").get_clubs().data()

    assert clubs[0].id == "/manchester-city/startseite/verein/281/saison_id/2024"
    assert clubs[1].id == "/fc-arsenal/startseite/verein/11/saison_id/2024"


def test_get_previous_clubs():

    clubs = TMQuery(cache_results=True).search_competition("premier league").get_clubs("2017").data()

    assert clubs[0].id == "/manchester-city/startseite/verein/281/saison_id/2017"
    assert clubs[1].id == "/fc-chelsea/startseite/verein/631/saison_id/2017"


def test_csv():

    csv = TMQuery(cache_results=True).search_competition("premier league").csv()

    assert csv.split("\n")[0] == "name, number_of_teams, number_of_players, foreigners, avg_mv, avg_age, mvp"
    assert csv.split("\n")[1] == "Premier League, 20 teams, 530, null, €22.16m, 26.5, /erling-haaland/profil/spieler/418560"
