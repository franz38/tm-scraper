# TMQuery
TMQuery is a declarative library for efficiently and intuitively scraping data from Transfermarkt.

## Installation

```bash
pip install tmquery
```

## Usage

```python
from tmquery import TMQuery

TMQuery().search_player("luis suarez").csv()
```
| name | height | citizenship | ... | foot | agent | joined | expires |
|------|--------|-------------|-----|------|-------|--|--|
| Luis Suárez | 1.82 m | Uruguay | ... | right | Relatives | Jan 1, 2024 | Dec 31, 2024 |

<br>

```python
TMQuery().search_club("barcelona").get_players().csv()
```

| name                  | date_of_birth     | place_of_birth  | height | citizenship       | position               | foot  | agent                                      | current_club                                | joined       | expires     | option | outfitter |
|-----------------------|-------------------|-----------------|--------|-------------------|------------------------|-------|--------------------------------------------|---------------------------------------------|--------------|-------------|--------|-----------|
| Marc-André ter Stegen | Apr 30, 1992 (32) | Mönchengladbach | 1.87 m | Germany           | Goalkeeper             | right | /roof/beraterfirma/berater/2295            | /fc-barcelona/startseite/verein/131         | Jul 1, 2014  | Jun 30, 2028| null   | adidas    |
| Iñaki Peña            | Mar 2, 1999 (25)  | Alicante        | 1.84 m | Spain             | Goalkeeper             | right | /wakai-sports/beraterfirma/berater/12120   | /fc-barcelona/startseite/verein/131         | Jan 30, 2022 | Jun 30, 2026| null   | Nike      |
| ...     | ... | ...        | ... | ...            | ...             | ... | ...      | ...         | ...  | ...| ...   | ...      |

<br>

## License

This project is licensed under the MIT License.