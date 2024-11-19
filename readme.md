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

| name        | date_of_birth     | place_of_birth | height | citizenship | position                | foot  | agent     | current_club                                | joined       | expires     | option                    | outfitter |
|-------------|-------------------|----------------|--------|-------------|-------------------------|-------|-----------|---------------------------------------------|--------------|-------------|---------------------------|-----------|
| Luis Suárez | Jan 24, 1987 (37) | Salto          | 1.82 m | Uruguay     | Attack - Centre-Forward | right | Relatives | /inter-miami-cf/startseite/verein/69261     | Jan 1, 2024  | Dec 31, 2024| Option for a further year | Puma      |

<br>

```python
TMQuery().search_club("barcelona").get_players(season="2010-11").csv()
```


| name                | date_of_birth     | place_of_birth           | height | citizenship | position               | foot  | agent                                      | current_club                                | joined       | expires     | option | outfitter |
|---------------------|-------------------|--------------------------|--------|-------------|------------------------|-------|--------------------------------------------|---------------------------------------------|--------------|-------------|--------|-----------|
| Víctor Valdés       | Jan 14, 1982 (42) | L’Hospitalet de Llobregat| 1.83 m | Spain       | Goalkeeper             | right | no agent                                   | /retired/startseite/verein/123              | Aug 17, 2017 | -           | null   | null      |
| Rubén Miño          | Jan 18, 1989 (35) | Cornellà de Llobregat    | 1.91 m | Spain       | Goalkeeper             | right | /footfeel-ism/beraterfirma/berater/4477    | /ue-cornella/startseite/verein/16196        | Aug 3, 2023  | Jun 30, 2025| null   | null      |
| José Manuel Pinto   | Nov 8, 1975 (49)  | El Puerto de Santa María | 1.85 m | Spain       | Goalkeeper             | right | null                                       | /retired/startseite/verein/123              | Jul 1, 2014  | -           | null   | null      |
| Gerard Piqué        | Feb 2, 1987 (37)  | Barcelona                | 1.94 m | Spain       | Defender - Centre-Back | right | /ac-talent/beraterfirma/berater/5041       | null                                        | Jan 1, 2023  | -           | null   | Nike      |
| ...     | ... | ...        | ... | ...            | ...             | ... | ...      | ...         | ...  | ...| ...   | ...      |


<br>

## License

This project is licensed under the MIT License.
