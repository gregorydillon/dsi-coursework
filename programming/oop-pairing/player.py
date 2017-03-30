class Player(object):

    def __init__(self, name, is_dealer, buy_in):
        self._name = name
        self._is_dealer = is_dealer
        self._buy_in = buy_in
        self._bank = buy_in
        self._hand = []
        self.current_bet = None

    def make_bet(self):
        # TODO: allow user to modify bet with input
        self.current_bet = min(self._bank, 5)

    def make_decision(self, max_hand_value):
        if self._is_dealer:
            if max_hand_value > 16:
                return 's'
            return 'h'

        else:
            print "you have the cards {}".format(self._hand)
            choice = raw_input('h/s')
            return choice

    def add_to_bank(self, amount):
        pass

    def add_to_hand(self, card):
        self._hand.append(card)

    def discard_hand(self):
        pass
