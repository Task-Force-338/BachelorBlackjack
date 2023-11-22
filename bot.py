from random import randint
from pyswip import Prolog
from blackjack import Player as BlackjackPlayer
from cards import BlackjackCard, init_blackjack_deck

prolog = Prolog()

bot_names = ["Prolog", "SPB9000", "Aigis", "Labrys", "Pathfinder", "Asimo", "Pepper", "Bender", "R2D2", "C3PO", "TARS", "KITT", "HAL9000", "GLaDOS", "Wheatley", "TARS", "Marvin", "Data", "Wall-E", "Eve", "Johnny5", "Robocop", "Chappie", "Sonny", "T-800", "T-1000", "T-X", "T-3000", "T-5000", "T-1000000"]

class BlackJackBot(BlackjackPlayer):
    def __init__(self):
        self.prolog = Prolog()
        self.prolog.consult("blackjack.pl")
        self.observedDeck = init_blackjack_deck()
        self.is_a_bot = True
        self.name = bot_names[randint(0, len(bot_names) - 1)]


    def get_action(self, player_cards, dealer_cards):

        for card in player_cards:
            self.observedDeck.remove(card)
        for card in dealer_cards:
            self.observedDeck.remove(card)

        for card in self.observedDeck:
            # add the possible cards to the prolog database
            self.prolog.assertz(f"card({card.rank.value}, {card.suit.value})")

        # add the player's cards to the prolog deck
            self.prolog.assertz(f"deck(Deck)")

        for soln in self.prolog.query("get_action(Action)"):
            return soln["Action"]
        return "stand"