import random
from tabulate import tabulate
from math import ceil


class Batsman:
    def __init__(self, name, trait: None | str, Batting_rating: int, Bowling_rating: int):
        self.trait = trait
        self.Batting_rating = Batting_rating
        self.Bowling_rating = Bowling_rating
        self.name = name
        self.run_scored = 0
        self.ball_played = 0
        self.fours = 0
        self.sixes = 0
        self.status = False

    def zero_run(self):
        self.ball_played += 1

    def hit_one(self):
        self.run_scored += 1
        self.ball_played += 1

    def hit_two(self):
        self.run_scored += 2
        self.ball_played += 1

    def hit_three(self):
        self.run_scored += 3
        self.ball_played += 1

    def hit_four(self):
        self.run_scored += 4
        self.ball_played += 1
        self.fours += 1

    def hit_six(self):
        self.run_scored += 6
        self.ball_played += 1
        self.sixes += 1

    def display_batting_stats(self):
        print(f"Batter name : {self.name}")
        print(f"Runs scored: {self.run_scored}")
        print(f"balls played: {self.ball_played}")

    def batsman_dismissed(self):
        self.ball_played += 1
        self.status = True


class Bowler:
    def __init__(self, name, perfection: int, Batting_rating: int, Bowling_rating: int):
        self.perfection = perfection
        self.Batting_rating = Batting_rating
        self.Bowling_rating = Bowling_rating
        self.name = name
        self.run_conceded = 0
        self.ball_bowled = 0
        self.wickets_taken = 0

    def dot_ball(self):
        self.ball_bowled += 1

    def one_conceded(self):
        self.run_conceded += 1
        self.ball_bowled += 1

    def two_conceded(self):
        self.run_conceded += 2
        self.ball_bowled += 1

    def three_conceded(self):
        self.run_conceded += 3
        self.ball_bowled += 1

    def four_conceded(self):
        self.run_conceded += 4
        self.ball_bowled += 1

    def six_conceded(self):
        self.run_conceded += 6
        self.ball_bowled += 1

    def wide_delivery(self):
        self.run_conceded += 1

    def fall_of_wicket(self):
        self.wickets_taken += 1
        self.ball_bowled += 1

    def display_bowling_stats(self):
        print(f"Bowler name : {self.name}")
        print(f"Runs conceded: {self.run_conceded}")
        print(f"balls bowled: {self.ball_bowled}")
        print(f"wickets taken: {self.wickets_taken}")


def overs_ball(total_balls):
    overs = int(total_balls // 6)
    balls = total_balls % 6
    return f"{overs}.{balls}"


def format_deliveries(all_deliveries, team_name):
    legal_options = [0, 1, 2, 3, 4, 6, 'Wkt']
    chunks = []
    current_over = []
    legal_deliveries_count = 0

    for delivery in all_deliveries:
        if delivery in legal_options:
            current_over.append(str(delivery))
            legal_deliveries_count += 1
        elif delivery == 'Wd':
            current_over.append('Wd')

        # Check the length after each legal delivery
        if legal_deliveries_count == 6:
            chunks.append(" ".join(current_over))
            current_over = []
            legal_deliveries_count = 0  # Reset the counter

    if current_over:
        chunks.append(" ".join(current_over))

    return team_name + " : " + " | ".join(chunks)


def batsmen_scorecard(batsmen_stats, team_name):
    scorecard_headers = ['Name', 'Runs', 'Balls', '4', '6', 'Strike Rate']
    # scorecard_data = [[batsman, stats['Runs'], stats['Balls'], stats['4'], stats['6']] for
    #                   batsman, stats in batsmen_stats.items()]

    scorecard_data = []

    for batsman, stats in batsmen_stats.items():
        runs = stats['Runs']
        balls = stats['Balls']
        fours = stats['4']
        sixes = stats['6']

        if balls > 0 and runs > 0:
            strike_rate = (runs / balls) * 100
        else:
            strike_rate = 0.000

        scorecard_data.append([batsman, runs, balls, fours, sixes, f"{strike_rate:.2f}"])

    print(f"\n--- {team_name} Batsman's Scorecard ---")
    print(tabulate(scorecard_data, headers=scorecard_headers))
    print("-------------------")


def bowlers_scorecard(bowlers_stats, team_name):
    scorecard_headers = ['Name', 'Overs', 'Runs', 'Wickets', 'Economy']
    scorecard_data = []

    for bowler, stats in bowlers_stats.items():
        overs = stats['Balls']
        overs = overs_ball(overs)
        runs = stats['Runs']
        wickets = stats['Wickets']

        if runs > 0:
            economy = (runs / stats['Balls']) * 6
        else:
            economy = 0.0

        scorecard_data.append([bowler, overs, runs, wickets, f"{economy:.2f}"])

    print(f"\n--- {team_name} Bowler's Scorecard ---")
    print(tabulate(scorecard_data, headers=scorecard_headers))
    print("-------------------")


def get_current_bowler(bowlers, bowler_list, index):
    if index < len(bowlers):
        current_bowler = bowlers[index]
    else:
        # If the index exceeds the length of bowlers list, repeat the bowler_list again
        bowlers += [Bowler(name, random.randint(1, 10), random.randint(50, 85), random.randint(20, 50)) for name in
                    bowler_list]
        current_bowler = bowlers[index]
    return current_bowler


def next_batsman(batsman_list: list, next_batsman_index, i_strike, striker_batter, non_striker_batter):
    next_batsman = next((batsman for batsman in batsman_list[next_batsman_index:] if
                         not batsman.status and batsman != striker_batter and batsman != non_striker_batter),
                        None)
    if next_batsman:
        batsman_list[i_strike] = next_batsman
        next_batsman_index += 1
        i_strike = (i_strike % 2) % len(batsman_list)
        return batsman_list[i_strike]  # Return both the new striker and updated index
    else:
        return "All out"


def handle_runs(striker_batter, runs, current_bowler, batsmen_stats, bowlers_stats):
    bowlers_stats[current_bowler.name]['Runs'] += runs
    bowlers_stats[current_bowler.name]['Balls'] += 1
    batsmen_stats[striker_batter.name]['Runs'] += runs
    batsmen_stats[striker_batter.name]['Balls'] += 1
    if runs == 4:
        batsmen_stats[striker_batter.name]['4'] += 1
    elif runs == 6:
        batsmen_stats[striker_batter.name]['6'] += 1

    if runs == 0:
        striker_batter.zero_run()
        current_bowler.dot_ball()
    elif runs == 1:
        striker_batter.hit_one()
        current_bowler.one_conceded()
    elif runs == 2:
        striker_batter.hit_two()
        current_bowler.two_conceded()
    elif runs == 3:
        striker_batter.hit_three()
        current_bowler.three_conceded()
    elif runs == 4:
        striker_batter.hit_four()
        current_bowler.four_conceded()
    elif runs == 6:
        striker_batter.hit_six()
        current_bowler.six_conceded()

    return batsmen_stats, bowlers_stats


def handle_wicket(striker_batter, current_bowler, batsmen_stats, bowlers_stats):
    current_bowler.fall_of_wicket()
    striker_batter.batsman_dismissed()
    batsmen_stats[striker_batter.name]['Balls'] += 1
    bowlers_stats[current_bowler.name]['Wickets'] += 1
    bowlers_stats[current_bowler.name]['Balls'] += 1
    return batsmen_stats, bowlers_stats


wicket = [0, 'Wkt']
boundaries = [4, 6, 'Wkt'],
short_run = [0, 1, 2, 3],
illegal_delivery = ['Wd']

probability_each_events = {
    "wicket": 10,
    "boundaries": 30,
    "short_run": 30,
    "illegal_delivery": 30
}


def equalize_probabilities(probabilities, key_to_increase, percentage_increment):
    increment = int(round((probabilities[key_to_increase] / 100) * percentage_increment))
    probabilities[key_to_increase] += increment

    all_rest_event = [key for key in probabilities if key != key_to_increase]
    num_events = len(all_rest_event)
    if num_events > 0:
        decrement_per_event = increment // num_events
        remainder = increment % num_events

        for event in all_rest_event:
            if remainder > 0:
                new_value = max(0, probabilities[event] - (decrement_per_event + 1))
                remainder -= 1
            else:
                new_value = max(0, probabilities[event] - decrement_per_event)
            probabilities[event] = new_value

    total_probability = sum(probabilities.values())
    if total_probability > 100:
        overage = total_probability - 100
        for event in probabilities:
            reduction = int(probabilities[event] * overage / total_probability)
            probabilities[event] -= reduction
            total_probability -= reduction

            if total_probability <= 100:
                break

    return probabilities


def realistic_function(current_strike_batter, current_bowler, probability_each_events: dict):
    Batting_rating = current_strike_batter.Batting_rating
    Bowling_rating = current_bowler.Bowling_rating
    trait = current_strike_batter.trait
    perfection = current_bowler.perfection

    if Batting_rating >= 75 and trait in ["Opener", "Orthodox"]:
        if perfection >= 8 and Bowling_rating >= 75:
            return equalize_probabilities(probability_each_events, "boundaries", 15)
        elif Bowling_rating >= 75 and 4 <= perfection < 8:
            return equalize_probabilities(probability_each_events, "short_run", 25)

    elif 60 <= Batting_rating <= 75 and trait == "Orthodox":
        if 60 <= Bowling_rating <= 75:
            if perfection >= 8:
                return equalize_probabilities(probability_each_events, "wicket", 15)
            elif 4 <= perfection < 8:
                return equalize_probabilities(probability_each_events, "short_run", 15)
    elif 45 <= Batting_rating <= 60 and trait == "Finisher":
        if perfection >= 8 and Bowling_rating >= 65:
            return equalize_probabilities(probability_each_events, "wicket", 15)
        elif 7 <= perfection >= 4:
            return equalize_probabilities(probability_each_events, "boundaries", 20)
        elif 4 < perfection >= 2:
            return equalize_probabilities(probability_each_events, "short_run", 20)
        elif perfection < 2:
            return equalize_probabilities(probability_each_events, "illegal_delivery", 20)
    elif Batting_rating < 45 and trait == "Lower Order":
        if perfection >= 8 and Bowling_rating >= 60:
            return equalize_probabilities(probability_each_events, "wicket", 25)
        elif 7 <= perfection >= 4 and Bowling_rating < 60:
            return equalize_probabilities(probability_each_events, "wicket", 15)
        elif 4 < perfection >= 2 and Bowling_rating < 60:
            return equalize_probabilities(probability_each_events, "short_run", 10)
    return equalize_probabilities(probability_each_events, "short_run", 10)


def generate_probability_dict(probability_values: dict):
    result_list = []
    for event, probability in probability_values.items():
        if event == "wicket":
            count = probability // 2
            remainder = probability % 2
            if remainder > 0:
                outcomes = [0] * count + ['Wkt'] * count + [0] * remainder
            else:
                outcomes = [0] * count + ['Wkt'] * count
            result_list.extend(outcomes)
        elif event == "boundaries":
            count = probability // 3
            remainder = probability % 3
            if remainder > 0:
                outcomes = [4] * count + [6] * count + ['Wkt'] * count + [4] * remainder
            else:
                outcomes = [4] * count + [6] * count + ['Wkt'] * count
            result_list.extend(outcomes)
        elif event == "short_run":
            count = probability // 4
            remainder = probability % 4
            if remainder > 0:
                outcomes = [0] * count + [1] * count + [2] * count + [3] * count + [0] * remainder
            else:
                outcomes = [0] * count + [1] * count + [2] * count + [3] * count
            result_list.extend(outcomes)
        elif event == "illegal_delivery":
            outcomes = ['Wd'] * probability
            result_list.extend(outcomes)

    return result_list


def inning_play(batter_list, bowlers_list, overs, probability_each_events: dict = None, target=None):
    i_strike, i_non_strike = 0, 1
    index = 0
    team_score, team_wicket = 0, 0
    current_bowler_index, next_batsman_index = -1, 2
    batsman_list = [
        Batsman(name=batsman["name"], trait=batsman["trait"], Batting_rating=batsman["Batting_rating"],
                Bowling_rating=batsman["Bowling_rating"]) for batsman
        in batter_list]
    bowlers = [Bowler(name=bowler["name"], perfection=bowler["perfection"], Batting_rating=bowler["Batting_rating"],
                      Bowling_rating=bowler["Bowling_rating"]) for bowler in
               (bowlers_list * int(overs / len(bowlers_list) + 1))[:overs]]
    batsmen_stats = {batsman.name: {'Runs': 0, 'Balls': 0, '4': 0, '6': 0} for batsman in batsman_list}
    bowlers_stats = {bowler.name: {'Balls': 0, 'Runs': 0, 'Wickets': 0} for bowler in bowlers}
    all_delivery = []
    legal_delivery = overs * 6
    total_delivery = 0

    total_ball = 0

    while total_delivery < legal_delivery:
        # runs = random.choice([1, 2, 3, 'Wkt', 'Wd', 0, 6, 4])
        striker_Batter = batsman_list[i_strike]
        non_striker_Batter = batsman_list[i_non_strike]
        current_bowler = get_current_bowler(bowlers, bowlers_list, index)

        if target and team_score >= target:
            batsmen_scorecard(batsmen_stats, "Australia")
            bowlers_scorecard(bowlers_stats, "India")
            over_played = overs_ball(total_ball)
            return team_score, team_wicket, float(over_played), all_delivery

        current_probabilities = probability_each_events.copy()
        result = realistic_function(striker_Batter, current_bowler, current_probabilities)
        probability_list = generate_probability_dict(result)

        runs = random.choice(probability_list)

        all_delivery.append(runs)

        if runs == "Wd":
            team_score += 1
            current_bowler.wide_delivery()
            bowlers_stats[current_bowler.name]['Runs'] += 1
            continue
        elif runs in [1, 2, 3, 4, 6, 0]:
            total_ball += 1
            team_score += runs
            total_delivery += 1
            batsmen_stats, bowlers_stats = handle_runs(striker_Batter, runs, current_bowler, batsmen_stats,
                                                       bowlers_stats)
        elif runs == 'Wkt':
            total_ball += 1
            total_delivery += 1
            if team_wicket < 10:
                batsmen_stats, bowlers_stats = handle_wicket(striker_Batter, current_bowler, batsmen_stats,
                                                             bowlers_stats)
                team_wicket += 1
                new_batsman = next_batsman(batsman_list, next_batsman_index, i_strike, striker_Batter,
                                           non_striker_Batter)
                if new_batsman == "All out":
                    print("Team all out")
                    break
                elif new_batsman:
                    striker_Batter = new_batsman

            if team_wicket >= 10:
                print("Team all out")
                break

        if current_bowler.ball_bowled % 6 != 0 and runs in [1, 3]:
            i_strike, i_non_strike = i_non_strike, i_strike
        if current_bowler.ball_bowled % 6 == 0 and runs not in [1, 3]:
            i_strike, i_non_strike = i_non_strike, i_strike
        if current_bowler.ball_bowled % 6 == 0:
            index += 1

    if target:
        batsmen_scorecard(batsmen_stats, "Australia")
        bowlers_scorecard(bowlers_stats, "India")
        over_played = overs_ball(total_ball)
        return team_score, team_wicket, float(over_played), all_delivery
    else:
        batsmen_scorecard(batsmen_stats, "India")
        bowlers_scorecard(bowlers_stats, "Australia")
        over_played = overs_ball(total_ball)
        return team_score, team_wicket, float(over_played), all_delivery


if __name__ == '__main__':
    overs = 5

    probability_each_events = {
        "wicket": 10,
        "boundaries": 30,
        "short_run": 30,
        "illegal_delivery": 30
    }

    indian_batter_list = [
        {"name": "Rohit", "trait": "Opener", "Batting_rating": 85, "Bowling_rating": 20},
        {"name": "Jaiswal", "trait": "Opener", "Batting_rating": 75, "Bowling_rating": 15},
        {"name": "Kohli", "trait": "Orthodox", "Batting_rating": 85, "Bowling_rating": 15},
        {"name": "Gill", "trait": "Opener", "Batting_rating": 75, "Bowling_rating": 10},
        {"name": "Rahul", "trait": "Orthodox", "Batting_rating": 80, "Bowling_rating": 0},
        {"name": "Bharat", "trait": "Orthodox", "Batting_rating": 65, "Bowling_rating": 0},
        {"name": "Jaddu", "trait": "Finisher", "Batting_rating": 60, "Bowling_rating": 60},
        {"name": "Axar", "trait": "Finisher", "Batting_rating": 50, "Bowling_rating": 65},
        {"name": "Ashwin", "trait": "Finisher", "Batting_rating": 45, "Bowling_rating": 75},
        {"name": "Bumrah", "trait": "Bowler", "Batting_rating": 30, "Bowling_rating": 85},
        {"name": "Siraj", "trait": "Bolwer", "Batting_rating": 20, "Bowling_rating": 75}
    ]

    australian_bowlers_list = [
        {"name": "Cummins", "perfection": random.randint(1, 10), "Batting_rating": 30, "Bowling_rating": 85},
        {"name": "Starc", "perfection": random.randint(1, 10), "Batting_rating": 30, "Bowling_rating": 85},
        {"name": "Zampa", "perfection": random.randint(1, 10), "Batting_rating": 15, "Bowling_rating": 80},
        {"name": "Maxwell", "perfection": random.randint(1, 10), "Batting_rating": 70, "Bowling_rating": 45},
        {"name": "Hazelwood", "perfection": random.randint(1, 10), "Batting_rating": 15, "Bowling_rating": 80}
    ]

    first_inning = inning_play(indian_batter_list, australian_bowlers_list, overs, probability_each_events, target=None)
    print(f"{first_inning[0]}/{first_inning[1]}, {first_inning[2]}")
    print("------------------------------------------End of innings-----------------------------------------")
    australian_batter_list = [
        {"name": "Warner", "trait": "Opener", "Batting_rating": 85, "Bowling_rating": 15},
        {"name": "Head", "trait": "Opener", "Batting_rating": 80, "Bowling_rating": 30},
        {"name": "Marsh", "trait": "Orthodox", "Batting_rating": 75, "Bowling_rating": 35},
        {"name": "Smith", "trait": "Orthodox", "Batting_rating": 85, "Bowling_rating": 20},
        {"name": "Labuschange", "trait": "Orthodox", "Batting_rating": 80, "Bowling_rating": 25},
        {"name": "Maxwell", "trait": "Finisher", "Batting_rating": 70, "Bowling_rating": 45},
        {"name": "Inglis", "trait": "Finisher", "Batting_rating": 70, "Bowling_rating": 0},
        {"name": "Cummins", "trait": "Lower Order", "Batting_rating": 30, "Bowling_rating": 85},
        {"name": "Hazelwood", "trait": "Lower Order", "Batting_rating": 15, "Bowling_rating": 80},
        {"name": "Starc", "trait": "Lower Order", "Batting_rating": 30, "Bowling_rating": 85},
        {"name": "Zampa", "trait": "Lower Order", "Batting_rating": 15, "Bowling_rating": 80}
    ]

    indian_bowlers = [
        {"name": "Bumrah", "perfection": random.randint(1, 10), "Batting_rating": 30, "Bowling_rating": 85},
        {"name": "Siraj", "perfection": random.randint(1, 10), "Batting_rating": 20, "Bowling_rating": 75},
        {"name": "Ashwin", "perfection": random.randint(1, 10), "Batting_rating": 45, "Bowling_rating": 75},
        {"name": "Axar", "perfection": random.randint(1, 10), "Batting_rating": 50, "Bowling_rating": 65},
        {"name": "Jaddu", "perfection": random.randint(1, 10), "Batting_rating": 60, "Bowling_rating": 60}
    ]
    second_inning = inning_play(australian_batter_list, indian_bowlers, overs, probability_each_events,
                                (first_inning[0] + 1))
    print(f"{second_inning[0]}/{second_inning[1]}, {second_inning[2]}")
    if first_inning[0] > second_inning[0]:
        print(f"India won the match by {first_inning[0] - second_inning[0]} runs.")
    elif first_inning[0] < second_inning[0]:
        print(f"Australia won the match by {10 - second_inning[1]} wickets.")
    else:
        print("It's a tie! score level")

    print("\n--- Over Summary ---")

    print(format_deliveries(first_inning[3], "India"))
    print(format_deliveries(second_inning[3], "Australia"))
