from tmquery.utils import list_to_csv


class MatchDTO:
    def __init__(self, match_day: str, date: str, time: str, home_team: str, home_team_id: str,
                 away_team: str, away_team_id: str, system: str, coach: str, coach_id: str, 
                 attendance: str, result: str, competition: str, competition_id: str):
        self.match_day = match_day
        self.date = date
        self.time = time
        self.home_team = home_team
        self.home_team_id = home_team_id
        self.away_team = away_team
        self.away_team_id = away_team_id
        self.system = system
        self.coach = coach
        self.coach_id = coach_id
        self.attendance = attendance
        self.result = result
        self.competition = competition
        self.competition_id = competition_id
    
    def __str__(self):
        return list_to_csv(
            [
                self.match_day, self.date, self.time, self.home_team, self.home_team_id, self.away_team,
                self.away_team_id, self.system, self.coach, self.coach_id, self.attendance, self.result,
            ]
        )

    def csv_header():
        return list_to_csv(
            ["match_day", "date", "time", "home_team", "home_team_id", "away_team", 
             "away_team_id", "system", "coach", "coach_id", "attendance", "result"]
        )