from cards import BlackjackCard, init_blackjack_deck
from random import randint
from bettercallsaul import UnderArrestException

class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.score = 0
        self.stand = False
        self.bust = False
        self.double = False
    
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
    
    def stand(self):
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

class Game:
    def __init__(self):
        self.deck = init_blackjack_deck()
        self.players = []
        self.dealer = Dealer()
        self.round = 0

    
    def __str__(self):
        return f"Round {self.round}: {self.players} and {self.dealer}"
    
    def __repr__(self):
        return f"Round {self.round}: {self.players} and {self.dealer}"
    
    def add_player(self, name):
        self.players.append(Player(name))
    
    def deal(self):
        for player in self.players:
            player.hit(self.deck)
            player.hit(self.deck)
        self.dealer.show(self.deck)
        self.dealer.calc_score()
    

if __name__ == "__main__":

    # if randint(0, 1) == 1:
    #     print("The police has raided the underground casino! You are arrested and charged with illegal gambling.")
    #     print("Better call Saul!")
    #     raise UnderArrestException("You are under arrest!")

    game = Game()
    #this is a test with a single player. who knows? i might wire this with websocket and make it multiplayer
    game.add_player(input("What is your name? "))
    game.deal()
    print(game)

    print(game.dealer)
    print(game.players[0])

    while not game.players[0].stand:
        if game.players[0].score == 21:
            print("You already have 21!")
            game.players[0].stand = True
            break

        if input("Hit or stand? ").lower() == "hit":
            game.players[0].hit(game.deck)
            print(game.players[0])
        else:
            game.players[0].stand = True
            print(game.players[0])
    
    if game.players[0].bust:
        print("You bust!")
    else:
        game.dealer.show(game.deck)
        print(game.dealer)
        while not game.dealer.stand:
            if game.dealer.score < 17:
                game.dealer.show(game.deck)
                print(game.dealer)
            else:
                game.dealer.stand = True
                print(game.dealer)
        
        if game.dealer.bust:
            print("Dealer busts!")
            print("You win!")
        else:
            if game.dealer.score > game.players[0].score:
                print("Dealer wins!")
            elif game.dealer.score < game.players[0].score:
                print("You win!")
            else:
                print("Push!")



    