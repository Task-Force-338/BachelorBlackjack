% cards thingy

suit(hearts).
suit(diamonds).
suit(clubs).
suit(spades).

% ranks

rank(ace).
rank(2).
rank(3).
rank(4).
rank(5).
rank(6).
rank(7).
rank(8).
rank(9).
rank(10).
rank(jack).
rank(queen).
rank(king).

% a card is a card if it has a suit and a rank

card(Suit, Rank) :-
    suit(Suit),
    rank(Rank).

% hmm whats the value of that card i wonder?

value(OutVal, Card(Suit, Rank)) :-
    %we dont care about the suit in Blackjack
    ( Rank = ace -> (OutVal is 11; OutVal is 1 );
     Rank = jack -> OutVal is 10 ;
     Rank = queen -> OutVal is 10 ;
     Rank = king -> OutVal is 10 ;
     otherwise -> OutVal is Rank
    ).