import webbrowser

class UnderArrestException(Exception):
    """Exception raised when a player is arrested for cheating, or when the police raids the casino.
    Can be catched by Lawyer objects."""
    
    def __init__(self, message):
        #if not handled properly, greets the player with a 3D animated video of Saul Goodman
        webbrowser.open("https://www.youtube.com/watch?v=gDjMZvYWUdo")