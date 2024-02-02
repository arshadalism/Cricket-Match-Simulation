import random


class Batsman:
    def __init__(self, name):
        self.name = name
        self.run_scored = 0
        self.bowl_played = 0
        self.dot_ball = 0
        self.fours = 0
        self.sixes = 0
        self.single = 0
        self.double = 0
        self.third = 0
        self.strike_rate = 0.0
        self.status = False

    def hit_runs(self, run_scored):
        self.bowl_played += 1
        if run_scored == 4:
            self.fours += 1
            self.run_scored += 4
        elif run_scored == 6:
            self.sixes += 1
            self.run_scored += 6
        elif run_scored == 1:
            self.single += 1
            self.run_scored += 1
        elif run_scored == 2:
            self.double += 1
            self.run_scored += 2
        elif run_scored == 0:
            self.dot_ball += 1
        elif run_scored == 'W':
            self.dismissed()
        elif run_scored == 3:
            self.third += 1
            self.run_scored += 3

        # self.strike_rate = (self.run_scored / self.bowl_played) * 100

    def dismissed(self):
        self.status = True

    def display_batting_stats(self):
        print(f"{self.name}'s batting stats")
        print(f"Runs scored: {self.run_scored}")
        print(f"Bowl played: {self.bowl_played}")
        print(f"fours: {self.fours}")
        print(f"Sixes: {self.sixes}")
        # print(f"Single: {self.single}")
        # print(f"Double: {self.double}")
        # print(f"Third: {self.third}")
        # print(f"Dot ball: {self.dot_ball}")
        if self.run_scored > 0:
            print(f"Strike rate: {(self.run_scored / self.bowl_played) * 100:.2f}")

        # print(f"Strike rates: {self.strike_rate}")

        print("-------------------")


class Bowler(Batsman):
    def __init__(self, name):
        super().__init__(name)
        self.over_bowled = 0.0
        self.bowl_bowled = 0
        self.dot_ball = 0
        self.run_conceded = 0
        self.wickets_taken = 0
        self.wides = 0
        self.maiden = 0
        self.economy = 0.0

    def bowl_delivery(self, runs):
        self.bowl_bowled += 1
        # overs, balls_left = self.overs_and_balls(self.bowl_bowled)
        if runs == 'W':
            self.take_wicket()
        else:
            self.run_conceded += runs

        if runs == 0:
            self.dot_ball += 1

        self.economy = (self.run_conceded / int(self.bowl_bowled)) * 6  # Update economy based on overs

        print(f"{runs} runs bowled!")

    def take_wicket(self):
        super().dismissed()
        self.wickets_taken += 1
        print("Wickets taken")

    def overs_and_balls(self, balls_bowled):
        overs = balls_bowled // 6
        balls_left = balls_bowled % 6
        return f"{overs}.{balls_left}"

    def display_bowling_stats(self):
        print(f"{self.name}'s bowling stats")
        print(f"Bowl_bowled: {self.bowl_bowled}")
        print(f"run_conceded: {self.run_conceded}")
        print(f"Wickets taken: {self.wickets_taken}")
        # print(f"Dots: {self.dot_ball}")
        print(f"Over bowled: {self.overs_and_balls(self.bowl_bowled)}")
        print(f"Economy: {self.economy:.2f}")
        print("-------------------")


def innings_play(batter_list, bowler_list, overs, target=None):
    batsman_list = [Batsman(name) for name in batter_list]

    bowlers = [Bowler(name) for name in (bowler_list * (overs // len(bowler_list) + 1))[:overs]]

    print("\n------ Batting ------")
    i_strike = 0
    i_non_strike = 1
    i = 0

    team_score = 0
    wickets_lost = 0

    total_ball = 0

    for _ in range(overs * 6):
        runs = random.choice([1, 2, 3, 4, 6, 'W'])
        current_batsman_strike = batsman_list[i_strike]
        current_batsman_non_strike = batsman_list[i_non_strike]

        # current_bowler = bowlers[i]
        if i < len(bowlers):
            current_bowler = bowlers[i]
        else:
            # If not, repeat the bowler_list again
            bowlers += [Bowler(name) for name in bowler_list]
            current_bowler = bowlers[i]

        current_bowler.bowl_delivery(runs)
        total_ball += 1
        # current_batsman_strike.hit_runs(runs)

        next_batsman_index = 2

        if runs == 'W':
            current_batsman_strike.dismissed()
            if wickets_lost < 10:
                wickets_lost += 1
                print(f"{current_batsman_strike.name} got out.")
                print(f"runs: {current_batsman_strike.run_scored}, ball_played: {current_batsman_strike.bowl_played}")
                next_batsman = next((batsman for batsman in batsman_list[next_batsman_index:] if
                                     not batsman.status and batsman != current_batsman_strike and batsman != current_batsman_non_strike),
                                    None)
                if next_batsman:
                    print(f"Next batsman: {next_batsman.name}")
                    batsman_list[i_strike] = next_batsman
                    next_batsman_index += 1
                    i_strike = (i_strike % 2) % len(batsman_list)
                    # i_non_strike = (i_strike + 1) % len(batsman_list)
                else:
                    print("All batsmen are out")
                    break
        # if runs != 'W':
        #     team_score += runs
        # current_batsman_strike.display_batting_stats()

        if target is not None and team_score >= target:
            overs_played = total_ball // 6 + total_ball % 6 / 10
            return team_score, wickets_lost, float(overs_played)

        current_bowler.bowl_delivery(runs)

        if runs != 'W':
            team_score += runs

        print("------Batting Striker--------")
        current_batsman_strike.hit_runs(runs)
        current_batsman_strike.display_batting_stats()

        print("-----Batting Non striker--------")
        current_batsman_non_strike.display_batting_stats()

        if (current_bowler.bowl_bowled % 6 != 0) and runs in [1, 3]:
            i_strike, i_non_strike = i_non_strike, i_strike

        # print("-----Batting Non striker--------")
        # current_batsman_non_strike.display_batting_stats()

        print('---------Bowling---------')
        current_bowler.display_bowling_stats()

        if (current_bowler.bowl_bowled % 6 == 0) and (runs not in [1, 3]):
            i_strike, i_non_strike = i_non_strike, i_strike

        if current_bowler.bowl_bowled % 6 == 0:
            i += 1

        print("Done")
        print("------------------------")

    overs_played = total_ball // 6 + total_ball % 6 / 10
    return team_score, wickets_lost, float(overs_played)


if __name__ == '__main__':
    overs = 4
    india_batter_list = ["Rohit", "Jaiswal", "Gill", "Kohli", "Iyer", "Rahul", "Jadeja", "Aksar", "Ashwin", "Bumrah",
                         "Siraj"]
    australia_bowler_list = ["Cummins", "Starc", "Hazelwood", "Zampa", "Maxwell"]
    first_inning = innings_play(india_batter_list, australia_bowler_list, overs)
    print(f"First Inning: {first_inning}")

    print("------------------------------------------End of innings-----------------------------------------")

    australia_batter_list = ["Warner", "Head", "Smith", "Labuschange", "Marsh", "Maxwell", "Inglish", "Starc",
                             "Cummins", "Zampa", "Hazelwood"]
    india_bowler_list = ["Bumrah", "Aksar", "Siraj", "Ashwin", "Jadeja"]

    # second_inning_target = first_inning[0] + 1
    second_inning = innings_play(australia_batter_list, india_bowler_list, overs, (first_inning[0] + 1))
    print(f"Second Inning: {second_inning}")

    print("\n--- Match Result ---")

    if first_inning[0] > second_inning[0]:
        print(f"India won the match by {first_inning[0] - second_inning[0]} runs.")
    elif first_inning[0] < second_inning[0]:
        print(f"Australia won the match by {10 - second_inning[1]} wickets.")
    else:
        print("It's a tie! score level")
