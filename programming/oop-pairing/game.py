from player import Player
from deck import Deck

class Game(object):

    def __init__(self):
        dealer = Player("Mr. Dealer", True, 0)
        player = Player("Tyler", False, 500)

        # TODO: Room for extension to more players, not implemented
        self.players = [player, dealer]
        self.deck = Deck()

    def start_game(self):
        pass

    def deal(self):
        for i in xrange(len(self.players) * 2):
            player_idx = i % len(self.players)
            self.players[player_idx].add_to_hand(self.deck.draw_card())


    def play_round(self):
        # Players Bet
        for player in self.players:
            if not player._is_dealer:
                player.make_bet()

        # Deal
        self.deal()

        # Players act until all have acted (skip if blackjack)
        for player in self.players:

            # Players can hit many times.
            continue_acting = True
            while(continue_acting):
                values = self.evaluate_hand(player._hand)
                print type(values)
                max_hand_value = max(values)

                # If busted -- quit
                if min(values) > 21:
                    break

                choice = player.make_decision(max_hand_value)

                if choice != 'h' and choice != 's':
                    continue_acting = True
                    print "Sorry, that was not a valid choice -- type H or S"
                elif choice == 'h':
                    continue_acting = True
                    player.add_to_hand(self.deck.draw_card())
                else:
                    continue_acting = False
            print player._hand, self.evaluate_hand(player._hand)

        # Determine winners and losers and BlkJack (and modify bank accounts)

    def end_game(self):
        pass

    def evaluate_hand(self, hand):
        hand_values = [0]
        for card in hand:
            card_values = card.get_card_values()
            new_values = []
            for old_value in hand_values:
                new_values.append(old_value + card_values[0])
                if len(card_values) == 2:
                    new_values.append(old_value + card_values[1])

            hand_values = new_values

        return hand_values


if __name__ == "__main__":
    print "works"
    g = Game()
    g.play_round()

    # test bet making
    for p in g.players:
        assert p._is_dealer or p.current_bet == 5
