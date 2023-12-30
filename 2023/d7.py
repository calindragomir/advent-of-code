from collections import Counter, namedtuple

import utils

sample = utils.Utilities.get_lines_from_file("sample/d7sample.txt")
full = utils.Utilities.get_full_input(__file__)

# lower the index higher the value
cardsP1 = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
cards_strengthP1 = {c: i for i, c in enumerate(cardsP1)}
cardsP2 = ['J', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'Q', 'K', 'A']
cards_strengthP2 = {c: i for i, c in enumerate(cardsP2)}

rules_strength = {
    (1, 1, 1, 1, 1): 0,
    (2, 1, 1, 1): 1,
    (2, 2, 1): 2,
    (3, 1, 1): 3,
    (3, 2): 4,
    (4, 1): 5,
    (5,): 6
}

CamelCard = namedtuple("CamelCard", "hand, game, bid")


def solvep1(lines):
    camelcards = []
    for line in lines:
        hand, bid = line.split(" ")
        c_hand = Counter(hand)
        camelcards.append(CamelCard(hand, apply_rule_get_points(c_hand, hand), bid))

    camelcards.sort(key=lambda c: (c.game[1], [cardsP1.index(a) for a in c.hand]))

    total_points = []
    for rank, camelcard in enumerate(camelcards):
        total_points.append((rank + 1) * int(camelcard.bid))
    return sum(total_points)


def solvep2(lines):
    camelcards = []
    for line in lines:
        hand, bid = line.split(" ")
        c_hand = Counter(hand)
        camelcards.append(CamelCard(hand, apply_rule_get_points_for_p2(c_hand, hand), bid))

    camelcards.sort(key=lambda c: (c.game[1], [cardsP2.index(a) for a in c.hand]))

    total_points = []
    for rank, camelcard in enumerate(camelcards):
        total_points.append((rank + 1) * int(camelcard.bid))
    return sum(total_points)


def apply_rule_get_points(c_hand, hand):
    sorted_cards = c_hand.most_common()
    points = tuple([v for k, v in sorted_cards])
    card_ranks = [(k, cards_strengthP1[k]) for k in hand]
    card_ranks.sort(key=lambda a: a[1], reverse=True)  # needs to be reversed to match the rule table
    return points, rules_strength[points], card_ranks


def get_highest_element_if_not_j(sorted_cards):
    k, v = sorted_cards[0]
    next_index = 1
    if k == 'J':
        k, v = sorted_cards[1]
        next_index = 2
    return k, v, next_index


def apply_rule_get_points_for_p2(c_hand, hand):
    sorted_cards = c_hand.most_common()
    points = []
    if 'J' in c_hand.elements() and len(c_hand) > 1:
        k, v, next_index = get_highest_element_if_not_j(sorted_cards)
        j = c_hand['J']
        points.append(v + j)
        points.extend([v for k, v in sorted_cards[next_index:] if k != 'J'])
    else:
        points.extend([v for k, v in sorted_cards])

    card_ranks = [(k, cards_strengthP2[k]) for k in hand]
    card_ranks.sort(key=lambda a: a[1], reverse=True)  # needs to be reversed to match the rule table
    return tuple(points), rules_strength[tuple(points)], card_ranks


if __name__ == '__main__':
    # print(solvep1(sample))
    # print(solvep1(full))
    # print(solvep2(sample))
    print(solvep2(full))
