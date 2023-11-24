from cards import BlackjackCard

class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.score = 0
        self.stand = False
        self.bust = False
        self.double = False
        self.is_a_bot = False
    
    def __str__(self):
        return f"{self.name} has {self.hand} for a score of {self.score}"
    
    def __repr__(self):
        return f"{self.name} has {self.hand} for a score of {self.score}"
    
    def hit(self, deck):
        self.hand.append(deck.pop())
        self.calc_score()
        if self.score > 21:
            self.bust = True
            self.stand = True
    
    def calc_score(self):
        self.score = 0
        num_aces = 0
        for card in self.hand:
            if isinstance(card, BlackjackCard):
                if card.rank == BlackjackCard.Rank.ACE:
                    num_aces += 1
                    continue
                self.score += card.value
        for i in range(num_aces):
            if self.score + 11 <= 21:
                self.score += 11
            else:
                self.score += 1
        if self.score > 21:
            self.bust = True
    
    def standup(self):
        self.stand = True

    def double_down(self, deck):
        self.hit(deck)
        self.stand = True
        self.double = True

class Dealer(Player):
    def __init__(self):
        super().__init__("Dealer")
        self.showing = []
    
    def __str__(self):
        return f"{self.name} has {self.showing} showing for a score of {self.score}"
    
    def __repr__(self):
        return f"{self.name} has {self.showing} showing for a score of {self.score}"
    
    def hit(self, deck):
        self.hand.append(deck.pop())
    
    def calc_score(self):
        self.score = 0
        num_aces = 0
        for card in self.showing:
            if isinstance(card, BlackjackCard):
                if card.rank == BlackjackCard.Rank.ACE:
                    num_aces += 1
                    continue
                self.score += card.value
        for i in range(num_aces):
            if self.score + 11 <= 21:
                self.score += 11
            else:
                self.score += 1
        if self.score > 21:
            self.bust = True
    
    def show(self, deck):
        if self.hand == []:
            self.hand.append(deck.pop())
        self.showing.append(self.hand.pop())
        self.calc_score()
        if self.score > 21:
            self.bust = True
            self.stand = True
        elif self.score >= 17:
            self.stand = True
