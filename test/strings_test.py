from tmquery.utils.strings import remove_season, get_season


def test_remove_season():
    assert remove_season("/manchester-city/startseite/verein/281/saison_id/2017") == "/manchester-city/startseite/verein/281"
    assert remove_season("/fc-chelsea/startseite/verein/631/saison_id/2017") == "/fc-chelsea/startseite/verein/631"
    assert remove_season("/as-rom/startseite/verein/12") == "/as-rom/startseite/verein/12"


def test_get_season():
    assert get_season("/manchester-city/startseite/verein/281/saison_id/2017") == "2017"
    assert get_season("/fc-chelsea/startseite/verein/631/saison_id/2005") == "2005"