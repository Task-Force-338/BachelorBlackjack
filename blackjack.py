from random import randint
from time import sleep as wait

from blackjackparticipant import Player, Dealer
from cards import BlackjackCard, init_blackjack_deck
from bettercallsaul import UnderArrestException
from bot import BlackJackBot, IntelligenceLevel

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
    if game.players[0].name.lower() == "prolog":
        print("Okay, then. Using the prolog bot instead.")
        print("How smart do you want the bot to be? 1-3")
        print("1: Basic Strategy. Hit if less than 17, stand if more than 17")
        print("2: Hard/Soft Strategy. Uses a lookup table to determine whether to hit or stand based on the dealer's card.")
        print("3: Deck Memory Strategy. Try to remember what cards have been played and use that to predict the next card. Something you can't do in real life without getting kicked out of the casino.")
        while True:
            level = int(input("Level: "))
            if level == 1:
                game.players[0] = BlackJackBot(IQLevel=IntelligenceLevel.LOW)
                break
            elif level == 2:
                game.players[0] = BlackJackBot(IQLevel=IntelligenceLevel.MEDIUM)
                break
            elif level == 3:
                game.players[0] = BlackJackBot(IQLevel=IntelligenceLevel.HIGH)
                break
            else:
                print("Invalid input. Try again.")
    game.deal()
    print(game)

    print(game.dealer)
    print(game.players[0])

    while not game.players[0].stand:
        if game.players[0].score == 21:
            print("You already have 21!")
            game.players[0].stand = True
            break
        
        if len(game.players[0].hand) == 2: # if the player has two cards, then they can double down
            if game.players[0].is_a_bot: # if the player is a bot, then use the bot's strategy note that the bot won't double down at all. it's too risky
                wait(1) # wait a second so that the player can see what's going on
                command = game.players[0].get_strategy(game.dealer.showing[0])
                if command == "hit":
                    game.players[0].hit(game.deck)
                    print("The bot hits.")
                    print(game.players[0])
                elif command == "stand":
                    game.players[0].standup()
                    print("The bot stands.")
                    print(game.players[0])
                else:
                    print("The bot spit random things.")
                    print(command)
            else: # if the player is a human, then ask them what they want to do
                command = input("Hit, stand, or double down? ").lower()
                if command == "hit" or command == "h":
                    game.players[0].hit(game.deck)
                    print(game.players[0])
                elif command == "stand" or command == "s":
                    game.players[0].standup()
                    print(game.players[0])
                elif command == "double down" or command == "double" or command == "dd":
                    game.players[0].double_down(game.deck)
                    print(game.players[0])
                else:
                    print("Invalid input. Try again.")

        else: # if the player has more than two cards, then they can only hit or stand
            if game.players[0].is_a_bot: # if the player is a bot, then use the bot's strategy
                wait(1)
                command = game.players[0].get_strategy(game.dealer.showing[0])
                if command == "hit":
                    game.players[0].hit(game.deck)
                    print("The bot hits.")
                    print(game.players[0])
                elif command == "stand":
                    game.players[0].standup()
                    print("The bot stands.")
                    print(game.players[0])
                else:
                    print("The bot spit random things.")
                    print(command)
            else: # if the player is a human, then ask them what they want to do
                command = input("Hit or stand? ").lower()
                if command == "hit" or command == "h":
                    game.players[0].hit(game.deck)
                    print(game.players[0])
                elif command == "stand" or command == "s":
                    game.players[0].standup()
                    print(game.players[0])
                else:
                    print("Invalid input. Try again.")
    
    if game.players[0].bust:
        print("The bot" if game.players[0].is_a_bot else "You", "bust!")
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
            print("The bot" if game.players[0].is_a_bot else "You", "win!")
        else:
            if game.dealer.score > game.players[0].score:
                print("Dealer wins!")
            elif game.dealer.score < game.players[0].score:
                print("The bot" if game.players[0].is_a_bot else "You", "win!")
            else:
                print("Push!")



    