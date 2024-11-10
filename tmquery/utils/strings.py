import re

season_pattern = r'\/saison_id\/\b\d{4}\b'

# removes season param from url 
# "/manchester-city/startseite/verein/281/saison_id/2017" -> "/manchester-city/startseite/verein/281"
def remove_season(url: str) -> str:
    return re.sub(season_pattern, "", url)


def get_season(url: str):
    m: str = re.findall(season_pattern, url)[0]
    return m.split("/")[-1]


def parse_season(raw: str) -> str:
    return raw