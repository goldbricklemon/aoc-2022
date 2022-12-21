# -*- coding: utf-8 -*-

ROCK = "Rock"
PAPER = "Paper"
SCISSORS = "Scissors"
RPS = [ROCK, PAPER, SCISSORS]

opponent_mapping = dict(zip(["A", "B", "C"], RPS))
own_mapping = dict(zip(["X", "Y", "Z"], RPS))
value_mapping = dict(zip(RPS, [1, 2, 3]))


def round_outcome(opponent, own):
    if opponent == own:
        return 3
    elif opponent == ROCK and own == PAPER:
        return 6
    elif opponent == PAPER and own == SCISSORS:
        return 6
    elif opponent == SCISSORS and own == ROCK:
        return 6
    else:
        return 0


def play_for_outcome(opponent, outcome):
    if outcome == PAPER:
        return opponent
    elif outcome == ROCK:
        return RPS[(RPS.index(opponent) - 1) % len(RPS)]
    else:
        return RPS[(RPS.index(opponent) + 1) % len(RPS)]


if __name__ == '__main__':
    with open("input.txt", "r") as f:
        lines = f.readlines()
    rounds = [(opponent_mapping[l[0]], own_mapping[l[2]]) for l in lines]

    print("#### Star one ####")
    score = 0
    for opponent, own in rounds:
        round_score = round_outcome(opponent, own) + value_mapping[own]
        score += round_score
    print(f"Score: {score}")

    print("#### Star two ####")
    score = 0
    for opponent, outcome in rounds:
        own = play_for_outcome(opponent, outcome)
        round_score = round_outcome(opponent, own) + value_mapping[own]
        score += round_score
    print(f"Score: {score}")
