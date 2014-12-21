import calendar

class Match:
    def __init__(self, date, home_team, away_team, home_team_score, away_team_score):
        """
        Given initialization data
        When I initialize a Match
        Then match properties are populated

        >>> test_match = Match("1/1/2014", "Everton", "Manchester City", 3, 1)

        >>> print(test_match.home_team)
        Everton

        >>> type(test_match.date)
        <class 'datetime.datetime'>

        >>> test_match.home_team_score
        3

        """
        self.home_team = home_team
        self.away_team = away_team
        self.date = calendar.datetime.datetime.strptime(date, "%d/%m/%Y")
        self.home_team_score = home_team_score
        self.away_team_score = away_team_score

    def __str__(self):
        return "\%s | \%s" % (self.home_team, self.away_team)

    def winner(self):
        """
            Determine the winner of the match

            Given match data
            When asking for a winner
            Then return the winner of the match
            And return None if it is a tie

            >>> Match("1/1/2014", "Everton", "Manchester City", 3, 1).winner()
            'Everton'

            >>> Match("1/1/2014", "Everton", "Manchester City", 1, 3).winner()
            'Manchester City'

            >>> Match("1/1/2014", "Everton", "Manchester City", 1, 1).winner()
        """
        if self.home_team_score > self.away_team_score:
            return self.home_team
        elif self.home_team_score < self.away_team_score:
            return self.away_team
        else:
            return None

    @staticmethod
    def load_data(match_data):
        """
            Load match data from a comma separated list of values.

            Given a comma separated list of soccer match data
            When I process the data with load_match_data
            Then a valid match object is created

            >>> test_data = "1/1/2014,Everton,Manchester City,3,1,1,1"
            >>> test_match = Match.load_data(test_data)
            >>> print(test_match.home_team)
            Everton

            >>> type(test_match.date)
            <class 'datetime.datetime'>

        """
        parsed_match_data = match_data.split(',')
        match = Match(parsed_match_data[0],
            parsed_match_data[1],
            parsed_match_data[2],
            parsed_match_data[3],
            parsed_match_data[4])
        return match


class MatchAnalyzer:

    def __init__(self, file_name):
        """
            Load match data file and return a list of matches.

            Given a CSV file with match data
            When I read the match data file
            And create Matchs from the data
            Then a list of valid Match objects are created

            >>> match_data = MatchAnalyzer("stats.csv").matches
            >>> len(match_data)
            2
        """
        self.matches = []
        data_file = open(file_name, 'r').readlines()
        for match in map(Match.load_data, data_file):
            self.matches.append(match)

    def number_of_matches(self):
        """
            Return the total number of matches loaded in the match analyzer

            Given the match analyzer has loaded data
            When I ask for the number of matches
            Then the total number of matches loaded is returned

            >>> match_analyzer = MatchAnalyzer("stats.csv")
            >>> match_analyzer.number_of_matches()
            2

        """
        return len(self.matches)

    def team_matches(self, team_name):
        """
            Get a list of matches by team name.

            Given the match analyzer has loaded data
            When I request a list of matches by team
            Then I get a list of matches the team is playing in (home or away)

            >>> match_analyzer = MatchAnalyzer("stats.csv")
            >>> len(match_analyzer.team_matches("Everton"))
            2
            >>> len(match_analyzer.team_matches("Stoke City"))
            1
            >>> len(match_analyzer.team_matches("NOT A REAL TEAM"))
            0
        """
        return [match for match in self.matches if (match.home_team == team_name or match.away_team == team_name)]

    def matches_won(self, team_name, include_ties=False):
        """
            >>> match_analyzer = MatchAnalyzer("stats.csv")
            >>> len(match_analyzer.matches_won("Everton"))
            1
            >>> len(match_analyzer.matches_won("Everton", True))
            2
            >>> len(match_analyzer.matches_won("Stoke City"))
            0
            >>> len(match_analyzer.matches_won("NOT A REAL TEAM"))
            0

        """

        team_matches = self.team_matches(team_name)
        if include_ties:
            wins = [match for match in team_matches if (match.winner() == team_name or match.winner() == None)]
        else:
            wins = [match for match in team_matches if match.winner() == team_name]
        return wins



if __name__ == "__main__":
    import doctest
    doctest.testmod()
