"""
This program accepts the soccer tournament result strings
and decides the rank and result of each tournament.
"""


import argparse


class Game:
    def __init__(self, game_text):
        """
        Game stores the game result information
        The constructor takes the string "team_name#goals@goals#team_name"
        The attributes are names and goals of players in a game
        :param game_text: a list of formatted string
        """
        self.player1, goals, self.player2 = game_text.split('#')
        goal1, goal2 = goals.split('@')
        self.goal1, self.goal2 = int(goal1), int(goal2)


class Scoreboard:
    def __init__(self, team_names):
        """
        Scoreboard stores the tournament result information.
        The constructor takes a list of game objects and a list of team names
        The attributes are:
        scores: map team name to raw game result including
            a list: a sequence of points standing for wins, ties, losses
            an int: total number of goals scored
            an int: total number of goals against
        info: map team name to formatted game result
        :param team_names: a list of team names
        """
        self.scores = dict([(team, [[], 0, 0]) for team in team_names])
        self.info = {}

    def write_scoreboard(self, results):
        """
        The method write raw game result in attribute scores
        :param results: a list of game objects
        :return: updated attribute scores dictionary
        """
        for result in results:  # write each game result into scores dict
            player1, goal1 = result.player1, result.goal1
            player2, goal2 = result.player2, result.goal2

            self.scores[player1][1] += goal1  # update goals scored and against
            self.scores[player1][2] += goal2
            self.scores[player2][1] += goal2
            self.scores[player2][2] += goal1

            if goal1 == goal2:  # if it is a tie
                self.scores[player1][0].append(1)
                self.scores[player2][0].append(1)
            elif goal1 > goal2:  # if player 1 wins
                self.scores[player1][0].append(3)
                self.scores[player2][0].append(0)
            else:  # if player 2 wins
                self.scores[player1][0].append(0)
                self.scores[player2][0].append(3)
        return self.scores

    def summarize_info(self):
        """
        The method summarize raw game result in attribute info
        :return: updated attribute info dictionary
        """
        for key in self.scores.keys():
            scored = self.scores[key][1]  # goals score
            against = self.scores[key][2]  # goals against
            wins = self.scores[key][0].count(3)  # number of wins
            ties = self.scores[key][0].count(1)  # number of ties
            losses = self.scores[key][0].count(0)  # number of losses
            points = 3 * wins + 1 * ties  # total points

            self.info[key] = [points, wins + ties + losses,
                              wins, ties, losses,
                              scored - against, scored, against]
        return self.info

    def rank(self):
        """
        The method sort the summarized info dict by sorting with DSU
        by creating an auxiliary list and using native sort functions

        auxiliary list sort with rules being:
        1) most points earned, v[0] points
        2) most wins, v[2] wins
        3) most goal difference: v[5] scored - against
        4) most goal scored: v[6] goals scored
        5) less game played: v[1] game played
        6) lexicographic order: k team name

        :return: sorted team_name list
        """
        to_sort = [(v[0], v[2], v[5], v[6], -v[1], k)
                   for k, v in self.info.items()]
        to_sort.sort(reverse=True)  # decreasing
        sorted_dict_keys = [item[-1] for item in to_sort]  # return sorted keys
        return sorted_dict_keys


class Tournament:
    def __init__(self, tournament_name, team_names, games_text):
        """
        Tournament manages the tournament games running, result
        updating, info summary, ranking and printing and writing
        :param tournament_name: tournament name string
        :param team_names: a list of team names
        :param games_text: a list of strings for games information
        """
        self.tournament_name = tournament_name
        self.games = [Game(t) for t in games_text]  # games in tournament
        self.num_teams = len(team_names)
        self.scoreboard = Scoreboard(team_names)  # create a scoreboard
        self.scoreboard.write_scoreboard(self.games)  # write games on scoreboard
        self.info = self.scoreboard.summarize_info()  # summarize scoreboard
        self.rank = self.scoreboard.rank()  # rank teams in tournament

    def print_result(self, output_file=None):
        """
        print on screen and write into text if required
        :param output_file: File handle to output a text file, default is None
        """
        ans_to_write = ""  # answer to write into file
        ans_to_write += (self.tournament_name+'\n')
        print(self.tournament_name)

        for i in range(self.num_teams):  # write team by team
            team = self.rank[i]
            team_res = (str(i + 1) + ") " + team + " " +
                        str(self.info[team][0]) + "p, " +
                        str(self.info[team][1]) + "g (" +
                        str(self.info[team][2]) + "-" +
                        str(self.info[team][3]) + "-" +
                        str(self.info[team][4]) + "), " +
                        str(self.info[team][5]) + "gd (" +
                        str(self.info[team][6]) + "-" +
                        str(self.info[team][7]) + ")")
            print(team_res)
            ans_to_write += (team_res+'\n')

        if output_file:  # if write_file is required
            output_file.write(ans_to_write)


def main():
    # parse input file
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    args = parser.parse_args()

    # prepare output file
    output = open("game_res.txt", "w+")  # create an txt file

    with open(args.filename, encoding='utf-16') as file:
        num_tournament = int(file.readline())
        for _ in range(num_tournament):
            # read input
            tournament_name = file.readline()[:-1]
            team_num = int(file.readline())
            team_names = [file.readline()[:-1] for __ in range(team_num)]
            game_num = int(file.readline())
            games_text = [file.readline()[:-1] for __ in range(game_num)]

            # run the program
            tournament = Tournament(tournament_name, team_names, games_text)
            tournament.print_result(output_file=output)

    output.close()


if __name__ == "__main__":
    main()











