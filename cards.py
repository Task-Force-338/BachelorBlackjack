from enum import Enum
from random import shuffle

class Card:

    class Suit(Enum):
        CLUBS = 1
        DIAMONDS = 2
        HEARTS = 3
        SPADES = 4
        
        def __str__(self):
            return self.name.capitalize()
        
        def __repr__(self):
            return self.name.capitalize()

    class Rank(Enum):
        TWO = 2
        THREE = 3
        FOUR = 4
        FIVE = 5
        SIX = 6
        SEVEN = 7
        EIGHT = 8
        NINE = 9
        TEN = 10
        JACK = 11
        QUEEN = 12
        KING = 13
        ACE = 14

        def __str__(self):
            return self.name.capitalize()

        def __repr__(self):
            return self.name.capitalize()

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.value = rank.value
    
    def __str__(self):
        return f"{self.rank} of {self.suit}"
    
    def __repr__(self):
        return f"{self.rank} of {self.suit}"
    
    def __eq__(self, other):
        return self.value == other.value
    
    def __lt__(self, other):
        return self.value < other.value
    
    def __gt__(self, other):
        return self.value > other.value
    
    def __le__(self, other):
        return self.value <= other.value
    
    def __ge__(self, other):
        return self.value >= other.value
    
    def __ne__(self, other):
        return self.value != other.value
    
def init_deck():
    deck = []
    for suit in Card.Suit:
        for rank in Card.Rank:
            deck.append(Card(rank, suit))
    shuffle(deck)
    return deck

class BlackjackCard(Card):
    def __init__(self, rank, suit):
        super().__init__(rank, suit)
        if rank == Card.Rank.JACK or rank == Card.Rank.QUEEN or rank == Card.Rank.KING:
            self.value = 10
        elif rank == Card.Rank.ACE:
            self.value = 11

def init_blackjack_deck():
    deck = []
    for suit in Card.Suit:
        for rank in Card.Rank:
            deck.append(BlackjackCard(rank, suit))
    shuffle(deck)
    return deck