import copy
from utils import Utilities

sample = Utilities.get_lines_from_file("sample/d4sample.txt")
lines = Utilities.get_lines_from_file("d4.txt")


class Card():
    def __repr__(self):
        return "Card %s: | won: %s | total_won: %s\n" % (self.card_id, self.won_cards, self.get_length())

    def __init__(self, card_id):
        self.card_id = card_id
        self.won_cards = []

    def add_won_cards(self, winners):
        self.won_cards.extend(winners)

    def get_won_cards_ids(self):
        return self.won_cards

    def get_length(self):
        return len(self.won_cards)


def solve(lines):
    total_points = []
    winning_cards = []
    scratchcards_winning = []
    for line in lines:
        cards, numbers = line.split(":")
        game_no = int(str(cards).lstrip("Card ").rstrip(":"))
        winning, extracted = numbers.split("|")
        winning_numbers = get_numbers(winning)
        extracted_numbers = get_numbers(extracted)
        winners = get_winning_numbers(extracted_numbers, winning_numbers)
        scratchcards_winning.append((game_no, len(winners)))
        do_part1(winning_cards, game_no, winners, total_points)

    print("part 1: %s" % sum(total_points))
    print("part 2: %s" % do_part2(scratchcards_winning))


def do_part1(winning_cards, game_no, winners, total_points):
    winning_cards.append((game_no, winners))
    points = calculate_points(winners)
    total_points.append(points)
    return total_points


def do_part2(scratchcards_winning):
    cards = {}

    for pair in scratchcards_winning:
        game_no, winners = pair
        c = Card(game_no)
        c.add_won_cards([i for i in range(game_no + 1, game_no + winners + 1)])
        cards[game_no] = c

    all_cards = get_all_cards(cards)
    return len(all_cards)


def get_all_cards(cards):
    all_cards = []
    cards_copy = copy.deepcopy(cards)
    still_to_process = []
    for i, c in cards_copy.items():
        still_to_process.append(c)

    while len(still_to_process) > 0:
        c = still_to_process.pop()
        all_cards.append(c.card_id)
        for card_id in c.get_won_cards_ids():
            still_to_process.append(cards[card_id])

    return all_cards


def calculate_points(winners):
    points = 0
    for i, point in enumerate(winners):
        if i == 0:
            points += 1
        else:
            points = points*2

    return points


def get_numbers(numbers_line):
    split = numbers_line.split(" ")
    return [i for i in split if i.isdigit()]


def get_winning_numbers(extracted, winning):
    return [i for i in extracted if i in winning]


if __name__ == '__main__':
    solve(sample)
    solve(lines)
