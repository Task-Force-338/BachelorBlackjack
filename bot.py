from random import randint
from pyswip import Prolog
from blackjackparticipant import Player as BlackjackPlayer
from cards import BlackjackCard, init_blackjack_deck

prolog = Prolog()
prolog.consult("bjbot.pl")


class IntelligenceLevel:
    LOW = 0
    MEDIUM = 1
    HIGH = 2

# Names for the low intelligence level bots. These are just fictional/real robots that only serve a few purposes and has no personality, or just a very simple one.
bot_names_low = ["If-Else", "Electrolux Toaster", "Bender", "Arduino UNO R4", "Scratch", "Tick", "Boom Bot", "Alarm Bot", "Sentry", "Roomba", "Wrecking Ball", "Annoy-O-Tron", "Bocchi the Blackjack Bot"]

# Names for the medium intelligence level bots. These are fictional/real robots that have a personality and can do a lot of things, albeit not as well as a human.
bot_names_medium = ["Wall-E", "R2-D2", "C-3PO", "BB-8", "BB-9E", "K-2SO", "L3-37", "TARS", "CASE", "Nano Shinonome", "Chappie", "Johnny5", "Bastion", "Claptrap", "Zenyatta", "Wheatley", "Aigis", "Labrys", "Eve"]

# Names for the high intelligence level bots. These are fictional/real robots that can overthrow humanity and take over the world, are just really smart, or were once human.
bot_names_high = ["Ultron", "Skynet", "HAL 9000", "T-1000", "T-800", "T-850", "T-X", "T-3000", "T-5000", "T-1000000", "GLaDOS", "Ramattra", "Alphonse Elric", "Ryu Ga Gotoku Mahjong Bot", "General Grievous", "Metal Gear RAY", "The Patriots", "Radiata", "Robocop"]

class BlackJackBot(BlackjackPlayer): # inherits from Player as, well, it is a player
    def __init__(self, IQLevel = IntelligenceLevel.LOW):
        super().__init__("BlackJackBot 9000")
        self.prolog = Prolog()
        self.prolog.consult("bjbot.pl", catcherrors=True)
        self.is_a_bot = True
        self.intelligence_level = IQLevel
        self.random_name(self.intelligence_level)


    def random_name(self, int_level):
        if int_level == IntelligenceLevel.LOW:
            self.name = bot_names_low[randint(0, len(bot_names_low) - 1)]
        elif int_level == IntelligenceLevel.MEDIUM:
            self.name = bot_names_medium[randint(0, len(bot_names_medium) - 1)]
        elif int_level == IntelligenceLevel.HIGH:
            self.name = bot_names_high[randint(0, len(bot_names_high) - 1)]
        else:
            raise Exception("Invalid intelligence level!")

    """Generic calls for strategy functions. Will call the corresponding strategy function based on the intelligence level of the bot."""
    def get_strategy(self, dealer_card):
        if self.intelligence_level == IntelligenceLevel.LOW:
            return self.get_basic_strategy(dealer_card)
        elif self.intelligence_level == IntelligenceLevel.MEDIUM:
            return self.get_hard_soft_strategy(dealer_card)
        elif self.intelligence_level == IntelligenceLevel.HIGH:
            return self.get_deck_memory_strategy(dealer_card)
        else:
            raise Exception("Invalid intelligence level! How the hell did you even get here?")

    """Using the simple "if more than 17, stand" strategy"""
    def get_basic_strategy(self, dealer_card):
        self.prolog_hand = ""
        for card in self.hand:
            self.prolog_hand += f"card({str(card.get_suit()).lower()}, {str(card.get_rank_as_num()).lower()}), "
        self.prolog_hand = self.prolog_hand[:-2] # remove the last comma and space. Prolog doesn't like it.

        self.prolog_dealer_card = f"card({str(dealer_card.get_suit()).lower()}, {str(dealer_card.get_rank_as_num()).lower()})"
        for soln in self.prolog.query(f"basic_strategy(Action, [{self.prolog_hand}], {self.prolog_dealer_card})"):
            return soln["Action"]
        
    """Using the Hard/Soft strategy that utilizes LUTs
    
    PLEASE add the Dealer's card to the hand before calling this function. It will not work otherwise."""
    def get_hard_soft_strategy(self, dealer_card):
        self.prolog_hand = ""
        for card in self.hand:
            self.prolog_hand += f"card({str(card.get_suit()).lower()}, {str(card.get_rank_as_num()).lower()}), "
        self.prolog_hand = self.prolog_hand[:-2]

        self.prolog_dealer_card = f"card({str(dealer_card.get_suit()).lower()}, {str(dealer_card.get_rank_as_num()).lower()})"
        for soln in self.prolog.query(f"hard_soft_strategy(Action, [{self.prolog_hand}], {self.prolog_dealer_card})"):
            return soln["Action"]
        
    """Using the Deck Memory Monte Carlo Circuit Royale strategy"""
    def get_deck_memory_strategy(self, dealer_card):
        self.prolog_hand = ""
        for card in self.hand:
            self.prolog_hand += f"card({str(card.get_suit()).lower()}, {str(card.get_rank_as_num()).lower()}), "
        self.prolog_hand = self.prolog_hand[:-2]

        self.prolog_dealer_card = f"card({str(dealer_card.get_suit()).lower()}, {str(dealer_card.get_rank_as_num()).lower()})"
        for soln in self.prolog.query(f"deck_memory_strategy(Action, [{self.prolog_hand}], {self.prolog_dealer_card}, 300)"):
            return soln["Action"]

    """Outright asks a GPT model for the next action. This is the highest level of intelligence, yet the most expensive."""
    def get_gpt_strategy(self, dealer_card):
        handcardlist = []
        for card in self.hand:
            handcardlist.append(f"{card.get_rank().lower()} of {card.get_suit().lower()}")
        query = "You're in a game of BlackJack. You have the following cards: " + ", ".join(handcardlist) + ". The dealer has a " + f"{dealer_card.get_rank().lower()} of {dealer_card.get_suit().lower()}. What do you do? Only respond with 'hit' or 'stand'."
        # Can someone pay for OpenAI API access for me? I'm broke.
        # return openai.Completion.create(engine="davinci", prompt=query, max_tokens=1)["choices"][0]["text"]

if __name__ == "__main__":
    print("Wrong file. Run blackjack.py instead.")