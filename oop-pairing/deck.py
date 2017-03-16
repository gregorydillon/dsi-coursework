import random

class Card(object):
    value_dict = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7,
                  '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12,
                  'K': 13, 'A': 14}

    def __init__(self, number, suit):
        self.suit = suit
        self.number = number

    def __repr__(self):
        return "%s%s" % (self.number, self.suit)

    def __cmp__(self, other):
        return cmp(self.value_dict[self.number], self.value_dict[other.number])

    def get_card_values(self):
        n = int(self.number)
        if n <= 10:
            return [n]
        elif n < 14 :
            return [10]
        else:
            return [1,11]


class Deck(object):
    def __init__(self):
        self.cards = []
        for num in Card.value_dict.keys():
            for suit in 'cdhs':
                self.cards.append(Card(num, suit))

    def shuffle(self):
        random.shuffle(self.cards)

    def draw_card(self):
        if not self.isempty():
            return self.cards.pop()

    def add_cards(self, cards):
        self.cards.extend(cards)

    def __len__(self):
        return len(self.cards)

    def isempty(self):
        return self.cards == []
