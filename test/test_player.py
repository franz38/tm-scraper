from tmquery.query.query import TMQuery


def test_get_data():
    
    player_data = TMQuery(cache_results=True).search_player("dybala").get_data()[0]
    
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
