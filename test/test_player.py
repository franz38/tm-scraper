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