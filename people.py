class Lawyer:
    """Lawyer class. Lawyers can bribe the police to get their clients out of jail. They can also represent their clients in court."""
    def __init__(self, name):
        self.name = name
        self.casino = None
        self.money = 0
        self.is_arrested = False

    def __str__(self):
        return self.name

    def join_casino(self, casino):
        """Joins a casino."""
        self.casino = casino

    def leave_casino(self):
        """Leaves a casino."""
        self.casino = None

    def get_money(self, amount):
        """Gets money from the casino."""
        self.money += amount

    def give_money(self, amount):
        """Gives money to the casino."""
        self.money -= amount

    #lawyers don't play

    def bribe(self, police):
        """Bribes the police to get the player out of jail."""
        if self.money >= 10000:
            self.give_money(10000)
            police.get_money(10000)
            self.is_arrested = False
            print(f"{self} bribed the police and is free to go!")
        else:
            print(f"{self} doesn't have enough money to bribe the police!")

    def get_arrested(self):
        """Gets arrested for cheating. The player is removed from the casino. Should be called as a result of an exception being raised."""
        self.is_arrested = True
        self.casino.remove_player(self)
        self.casino = None
        print(f"{self} was arrested for cheating!")

    def get_raided(self):
        """Gets arrested for being in an illegal casino. The player is removed from the casino. Should be called as a result of an exception being raised."""
        self.is_arrested = True
        self.casino.remove_player(self)
        self.casino = None
        print(f"{self} was arrested for being in an illegal casino!")

    def OBJECT(self):
        """Raises an objection. Bonus points if the lawyer's name is the following:
        Phoenix Wright
        Miles Edgeworth
        Franziska von Karma
        Godot
        Apollo Justice
        Athena Cykes
        Simon Blackquill
        Nahyuta Sahdmadhi
        Klavier Gavin
        Kristoph Gavin
        Mia Fey
        Marvin Grossberg
        Diego Armando
        Winston Payne
        """
        print("OBJECTION!")

johnjudgment = Lawyer("Takayuki Yagami")
saulgoodman = Lawyer("Saul Goodman")
acephoenix = Lawyer("Phoenix Wright")
autopsyreport = Lawyer("Miles Edgeworth") #isn't he a prosecutor?
mikemcmanus = Lawyer("Mike McManus")

class Player:
    """Generic Player class that can join other games. Once joined a game, they use the scoring system of the respective Game object they joined."""
    def __init__(self, name):
        self.name = name
        self.game = None
        self.cash = 0
        self.chips = 0
        self.is_arrested = False

    def __str__(self):
        return self.name
    
    def join_game(self, game):
        """Joins a game."""
        self.game = game
    
    def leave_game(self):
        """Leaves a game."""
        self.game = None

    def get_cash(self, amount):
        """Gets cash from the casino."""
        self.cash += amount

    def give_cash(self, amount):
        """Gives cash to the casino."""
        self.cash -= amount

    def get_chips(self, amount):
        """Gets chips from the casino."""
        self.chips += amount
    
    def give_chips(self, amount):
        """Gives chips to the casino."""
        self.chips -= amount

    def get_arrested(self):
        """Gets arrested for cheating. The player is removed from the game. Should be called as a result of an exception being raised."""
        self.is_arrested = True
        self.game.remove_player(self)
        self.game = None
        print(f"{self} was arrested for cheating!")

    def get_raided(self):
        """Gets arrested for being in an illegal casino. The player is removed from the game. Should be called as a result of an exception being raised."""
        self.is_arrested = True
        self.game.remove_player(self)
        self.game = None
        print(f"{self} was arrested for being in an illegal casino!")

    
dragon = Player("Kazuma Kiryu")
phoenix = Player("Shun Akiyama")
tiger = Player("Taiga Saejima")
tortoise = Player("Masayoshi Tanimura") #isn't he a cop? can he even get arrested?
baseballplayer = Player("Tatsuo Shinada")
maddog = Player("Goro Majima")
detective = Player("Makoto Date") #isn't he a cop? can he even get arrested? #nvm he left the force