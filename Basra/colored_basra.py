import random
import itertools
import colored as colored
from colored import stylize


def instructions():
    print(stylize('Your cards are blue', colored.fg("blue")))
    print(stylize('Computer card is red', colored.fg("red")))
    print(stylize('Ground cards are green', colored.fg("green")))
    print(stylize('Game status are yellow', colored.fg("yellow")))
    print('To select a card choose its position (1, 2, 3 or 4)')
    print()


def colored_basra(word):
    for i in word:
        color_range = str(random.randint(0, 255))
        print(stylize(i, colored.fg(color_range)), end='')
    print()


def first_hand_ground(deck):
    ground = random.sample(deck[:47], k=4)
    for card in ground:
        deck.remove(card)
    return ground, deck


def give_4_cards_each(deck):
    player_cards = random.sample(deck, k=4)
    for card in player_cards:
        deck.remove(card)
    return player_cards, deck


def is_jack_basra(card, ground):
    if card == 'J' and ground == ['J']:
        return True
    return False


def direct_basra(ground, card):
    try:
        if ['7c'] == ground:
            return True
        if [card] == ground:
            return True
        if ground == [card] * len(ground):
            return True
        if ('K' not in ground) and ('Q' not in ground) and (card != 'K') and (card != 'Q') and (card != '7c') \
                and (card != 'J') and (sum(list(map(int, ground))) == int(card)):
            return True
    except:
        return False


def get_combinations(ground):
    combinations = []
    for i in range(len(ground) + 1, 1, -1):
        combinations += itertools.combinations(ground, i)
    combinations_sums = list(map(sum, combinations))
    return combinations, combinations_sums


def get_combinations_ground(ground):
    combinations = []
    for i in range(len(ground) + 1, 1, -1):
        combinations += itertools.permutations(ground, i)
    return combinations


def combination_basra(ground, card):
    try:
        g = list(map(int, ground))
        combinations, combinations_sums = get_combinations(g)
        while int(card) in combinations_sums:
            for i in range(len(combinations)):
                if combinations_sums[i] == int(card):
                    for c in combinations[i]:
                        g.remove(c)
                    break
            combinations, combinations_sums = get_combinations(g)
        if len(g) == 0:
            return True
    except:
        return False


def best_eat_not_numbers(ground, card):
    g = ground.copy()
    eaten_cards = g.count(card)
    for _ in range(g.count(card)):
        g.remove(card)
    if eaten_cards != 0:
        return g, eaten_cards + 1
    return g, eaten_cards


def best_eat_numbers(ground, card):
    eaten_cards = 0
    integers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
    not_integers = ['Q', 'K', 'J']
    g_all = sorted(ground)
    g = [int(i) for i in g_all if i in integers]
    g_not_integers = [i for i in g_all if i in not_integers]
    combinations, combinations_sums = get_combinations(g)

    if int(card) in g:
        for _ in range(g.count(int(card))):
            g.remove(int(card))
            eaten_cards += 1

    while int(card) in combinations_sums:
        for i in range(len(combinations)):
            if combinations_sums[i] == int(card):
                for c in combinations[i]:
                    g.remove(c)
                    eaten_cards += 1
                break
        combinations, combinations_sums = get_combinations(g)

    if eaten_cards != 0:
        return list(map(str, g)) + g_not_integers, eaten_cards + 1
    return list(map(str, g)) + g_not_integers, eaten_cards


def is_comey_basra(ground, card='7c'):
    integers = [1, 2, 3, 4, 5, 6, 8, 9, 10]
    if card == '7c' and len(ground) == 1:
        return True
    for c in integers:
        if direct_basra(ground, c):
            return True
        if combination_basra(ground, c):
            return True
    return False


def single_hand(ground, chosen_card):
    g = ground.copy()
    score = 0
    cards = 0

    if len(g) == 0:
        g.append(chosen_card)
        return g, cards, score

    elif chosen_card == '7c':
        if is_comey_basra(g):
            cards += len(g) + 1
            score += 10
            g.clear()
        else:
            cards += len(g) + 1
            g.clear()

    elif is_jack_basra(chosen_card, g):
        cards += len(g) + 1
        score += 30
        g.clear()

    elif chosen_card == 'J':
        cards += len(g) + 1
        g.clear()

    elif direct_basra(g, chosen_card) or combination_basra(g, chosen_card):
        cards += len(g) + 1
        score += 10
        g.clear()

    else:
        if chosen_card == 'Q' or chosen_card == 'K':
            g, eaten_cards = best_eat_not_numbers(g, chosen_card)
            cards += eaten_cards
        else:
            g, eaten_cards = best_eat_numbers(g, chosen_card)
            cards += eaten_cards

    if cards == 0:
        g.append(chosen_card)

    return g, cards, score


def best_choice(ground, second_cards):
    scores = []
    cards = []
    for card in second_cards:
        _, c, s = single_hand(ground, card)
        cards.append(c)
        scores.append(s)
    if max(scores) != 0:
        return second_cards[(scores.index(max(scores)))]
    elif max(cards) != 0:
        return second_cards[(cards.index(max(cards)))]
    else:
        if 'Q' in second_cards:
            return 'Q'
        if 'K' in second_cards:
            return 'K'
        else:
            return min(second_cards)


def main():
    while True:
        try:
            foura = int(input('Set a target foura (a score which who reaches first wins): '))
            if foura < 10:
                print('foura must be greater than 10')
                continue
            break
        except:
            print('Choose a valid value')

    first_score = 0
    first_cards = []
    first_cards_sum = 0
    second_score = 0
    second_cards = []
    second_cards_sum = 0
    last_eater = ''
    deck = ['1', '2', '3', '4', '5', '6', '8', '9', '10', 'Q', 'K'] * 4 + ['7'] * 3 + ['7c'] + ['J'] * 4
    instructions()
    while (first_score < foura and second_score < foura) or (first_score == second_score):

        ground, deck = first_hand_ground(deck)
        for _ in range(6):
            print(stylize(ground, colored.fg("green")))
            first_cards, deck = give_4_cards_each(deck)
            second_cards, deck = give_4_cards_each(deck)
            for _ in range(4):
                print(stylize(first_cards, colored.fg("blue")))
                while True:
                    try:
                        chosen_card_first = first_cards[int(input('Select a card: ')) - 1]
                        break
                    except:
                        print('Choose a valid card')

                first_cards.remove(chosen_card_first)

                ground, cards, score = single_hand(ground, chosen_card_first)
                first_cards_sum += cards
                first_score += score
                if score == 10:
                    colored_basra('basra!')
                elif score == 30:
                    colored_basra('basra with jake!')
                if cards != 0:
                    last_eater = 'f'
                print(stylize(ground, colored.fg("green")))

                chosen_card_second = best_choice(ground, second_cards)
                second_cards.remove(chosen_card_second)
                ground, cards, score = single_hand(ground, chosen_card_second)
                second_cards_sum += cards
                second_score += score
                print(stylize(chosen_card_second, colored.fg("red")))
                if score == 10:
                    colored_basra('basra!')
                elif score == 30:
                    colored_basra('basra with jake!')
                if cards != 0:
                    last_eater = 's'

                print(stylize(ground, colored.fg("green")))

            print(stylize('First player cards = {}, and his score = {}'.format(first_cards_sum, first_score),
                          colored.fg("yellow")))
            print(stylize('Computer cards = {}, and his score = {}'.format(second_cards_sum, second_score),
                          colored.fg("yellow")))

        if last_eater == 'f':
            first_cards_sum += len(ground)
        elif last_eater == 's':
            second_cards_sum += len(ground)

        if first_cards_sum > second_cards_sum:
            first_score += 30
        elif first_cards_sum < second_cards_sum:
            second_score += 30

        print(stylize('Final first player cards = {}, and his score = {}'.format(first_cards_sum, first_score),
                      colored.fg("yellow")))
        print(stylize('Final computer cards = {}, and his score = {}'.format(second_cards_sum, second_score),
                      colored.fg("yellow")))

        first_cards_sum = 0
        second_cards_sum = 0
        last_eater = ''
        deck = ['1', '2', '3', '4', '5', '6', '8', '9', '10', 'Q', 'K'] * 4 + ['7'] * 3 + ['7c'] + ['J'] * 4


if __name__ == "__main__":
    main()
