from functools import reduce

from utils import Utilities

games_sample = Utilities.get_lines_from_file("sample/d2p1sample.txt")
games = Utilities.get_lines_from_file("d2.txt")

# 12 red cubes, 13 green cubes, and 14 blue cubes
LIMITS = {
    "blue": 14,
    "red": 12,
    "green": 13
}


def solve(games):
    total = 0
    for game in games:
        total += get_gameId_below_limit(game)
    return total

def solve2(games):
    total_mul = 0
    for game in games:
        total_mul += get_multiplier_per_game(game)
    return total_mul

def check_game(balls):
    for ball in balls.keys():
        if balls[ball] > LIMITS[ball]:
            return False
    return True


def get_gameId_below_limit(game):
    game_input = game.split(":")
    gameId = get_game_id(game_input)
    rounds = str(game_input[1]).strip().split(";")
    return check_not_exceeds_limits(rounds, gameId)


def get_game_id(game_input):
    return int(str(game_input[0]).strip().replace("Game ", ""))


def get_multiplier_per_game(game):
    game_input = game.split(":")
    rounds = str(game_input[1]).strip().split(";")
    balls = {}
    for round in rounds:
        extracted_balls = [r.strip() for r in round.split(",")]
        for extracted_ball in extracted_balls:
            counter, color = extracted_ball.split(" ")
            if color in balls.keys():
                if balls[color] < int(counter):
                    balls[color] = int(counter)
            else:
                balls[color] = int(counter)

    return reduce((lambda x, y: x * y), balls.values())



def check_not_exceeds_limits(rounds, gameId):
    for round in rounds:
        extracted_balls = [r.strip() for r in round.split(",")]
        for extracted_ball in extracted_balls:
            counter, color = extracted_ball.split(" ")
            if int(counter) > LIMITS[color]:
                return 0

    return gameId


if __name__ == '__main__':
    print(solve(games_sample))
    print(solve(games))
    print(solve2(games_sample))
    print(solve2(games))
