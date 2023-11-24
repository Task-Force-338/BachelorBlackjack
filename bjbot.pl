% suits

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
% OutVal is the value of the card, this is an output
% Card is the card to get the value of

value(OutVal, Card(Suit, Rank)) :- % literally just check the rank and assign a value
    %we dont care about the suit in Blackjack
    ( Rank = ace -> (OutVal is 11; OutVal is 1 );
    Rank = jack -> OutVal is 10 ;
    Rank = queen -> OutVal is 10 ;
    Rank = king -> OutVal is 10 ;
    otherwise -> OutVal is Rank
    ).

% score of a hand
% OutScore is the score of the hand, this is an output
% Hand is the hand to score

score(OutScore, Hand) :- % call helper with initial score of 0
    score(0, OutScore, Hand).
score(InScore, OutScore, [Card|Rest]) :- % bread and butter of the score function
    value(CardVal, Card),
    NewScore is InScore + CardVal,
    score(NewScore, OutScore, Rest).
score(InScore, OutScore, []) :- % recursion base case: empty hand
    OutScore is InScore.

% deck
% Deck is the generated deck, this is an output
% NOTE: this is a single deck, not a shoe.

deck(Deck) :- % generate a deck of cards
    findall(Card(Suit, Rank), card(Suit, Rank), Deck).

% remove card from deck, used in deck memory play
% Card is the card to remove
% Deck is the deck to remove from
% NewDeck is the deck after removal, this is an output
remove_card(Card, Deck, NewDeck) :-
    select(Card, Deck, NewDeck), !. % choose a card, select it, do nothing, then cut
% or just use subtract predicate lol

% shuffle deck, one of the most important functions in deck memory play
% Deck is the deck to shuffle
% NewDeck is the shuffled deck, this is an output
% Count is the number of times to shuffle, default is 100 for a good shuffle
% NOTE: I do not care what algorithm is used to shuffle, as long as it is random, it's fine. Real casinos use a machine to shuffle, so it's not like it matters.

shuffle(Deck, NewDeck) :- % call helper with default shuffle count of 100
    shuffle(Deck, NewDeck, 100).

shuffle(Deck, NewDeck, Count) :- % call helper but with a count
    Count > 0,
    random_permutation(Deck, TempDeck),
    NewCount is Count - 1,
    shuffle(TempDeck, NewDeck, NewCount).

shuffle(Deck, Deck, 0). % recursion base case: count is 0

% check if the player has ace in hand
% Hand is the hand to check
% HasAce is the output, true if the player has an ace, false otherwise
% used to determine if the player has a soft hand

has_ace(Hand, HasAce) :- % call helper with initial HasAce of false
    aggregate_all(count, member(Card(_,ace), Hand), Count), % count the number of aces in the hand
    ( Count > 0 -> HasAce = true ; otherwise HasAce = false ). % if the count is greater than 0, then the player has an ace. otherwise, the player does not have an ace.

% check the score of dealer's hand. mostly just a single card because the only time the dealer has more than 1 card is when everyone has standed
% DealerHand is the dealer's hand
% DealerScore is the score of the dealer's hand, this is an output

dealer_score(DealerScore, [_, card(_,Rank)]) :- % if the dealer has only 1 card, then just get the value of that card
    value(DealerScore, card(_,Rank)).
% if the dealer somehow has an ace
dealer_score(ace, [_, card(_,ace)]) :- % if the dealer has an ace, just return ace
    !.

% AI player strategies starts here.
% You could set what strat the bot will use in the Python code.
% By default, Pentium II will use basic strategy.
% Johnny 5 will use hard/soft total strategy.
% T-800 will use deck memory strategy.

% basic strategy
% Strategy is the strategy to use
% Hand is the hand to use the strategy on
% DealerCard is the dealer's card

% to call, use basic_strategy(Strategy, Hand, DealerCard). Strategy will be either hit or stand. Double down and split are not implemented because it is too risky.

basic_strategy(hit, Hand, DealerCard) :- % hit if score is less than 17. yeah i know its kinda dumb
    score(Score, Hand),
    Score < 17.

basic_strategy(stand, Hand, DealerCard) :- % stand if score is greater than or equal to 17
    score(Score, Hand),
    Score >= 17.

% hard/soft total strategy
% Strategy is the strategy to use
% Hand is the hand to use the strategy on
% DealerCard is the dealer's card

% to call, use hard_soft_strategy(Strategy, Hand, DealerCard). Strategy will be either hit or stand. Double down and split are not implemented because it is too risky.
hard_soft_strategy(Strategy, Hand, DealerCard) :- % call helper with initial HasAce of false
    has_ace(Hand, HasAce),
    dealer_score(DealerScore, DealerCard),
    score(Score, Hand),!, % only get the score once, treat ace as 11
    hard_soft_strategy(Strategy, Score, DealerScore, HasAce).

% it is hard if the player does not have an ace
hard_soft_strategy(Strategy, Score, DealerScore, false) :- % call helper with initial HasAce of false
    hard_strategy(Strategy, Score, DealerScore).

% it is soft if the player has an ace
hard_soft_strategy(Strategy, Score, DealerScore, true) :- % call helper with initial HasAce of false
    AdjustedScore is Score - 11, % adjust the score by subtracting 11, ignoring the ace
    hard_strategy(Strategy, AdjustedScore, DealerScore).

% very hardcoded list of all hard totals
% strategy(Do this if, if score is, dealer has)
% Strategy is the strategy to use, this is an output
% Score is the score of the player's hand
% DealerScore is the score of the dealer's hand

% hard strats requires the player to think that the dealer could have an ace in the hole.
% dealer has 2, stand at 13
hard_strategy(hit, 4, 2).
hard_strategy(hit, 5, 2).
hard_strategy(hit, 6, 2).
hard_strategy(hit, 7, 2).
hard_strategy(hit, 8, 2).
hard_strategy(hit, 9, 2).
hard_strategy(hit, 10, 2).
hard_strategy(hit, 11, 2).
hard_strategy(hit, 12, 2).
hard_strategy(stand, 13, 2).
hard_strategy(stand, 14, 2).
hard_strategy(stand, 15, 2).
hard_strategy(stand, 16, 2).
hard_strategy(stand, 17, 2).
hard_strategy(stand, 18, 2).
hard_strategy(stand, 19, 2).
hard_strategy(stand, 20, 2).
% most of the time if not all the Python part will automatically stand if the score is equal to or greater than 21, so I don't need to add it here.

% dealer has 3, stand at 13
hard_strategy(hit, 4, 3).
hard_strategy(hit, 5, 3).
hard_strategy(hit, 6, 3).
hard_strategy(hit, 7, 3).
hard_strategy(hit, 8, 3).
hard_strategy(hit, 9, 3).
hard_strategy(hit, 10, 3).
hard_strategy(hit, 11, 3).
hard_strategy(hit, 12, 3).
hard_strategy(stand, 13, 3).
hard_strategy(stand, 14, 3).
hard_strategy(stand, 15, 3).
hard_strategy(stand, 16, 3).
hard_strategy(stand, 17, 3).
hard_strategy(stand, 18, 3).
hard_strategy(stand, 19, 3).
hard_strategy(stand, 20, 3).

% dealer has 4, stand at 12
hard_strategy(hit, 4, 4).
hard_strategy(hit, 5, 4).
hard_strategy(hit, 6, 4).
hard_strategy(hit, 7, 4).
hard_strategy(hit, 8, 4).
hard_strategy(hit, 9, 4).
hard_strategy(hit, 10, 4).
hard_strategy(hit, 11, 4).
hard_strategy(stand, 12, 4).
hard_strategy(stand, 13, 4).
hard_strategy(stand, 14, 4).
hard_strategy(stand, 15, 4).
hard_strategy(stand, 16, 4).
hard_strategy(stand, 17, 4).
hard_strategy(stand, 18, 4).
hard_strategy(stand, 19, 4).
hard_strategy(stand, 20, 4).

% dealer has 5, stand at 12
hard_strategy(hit, 4, 5).
hard_strategy(hit, 5, 5).
hard_strategy(hit, 6, 5).
hard_strategy(hit, 7, 5).
hard_strategy(hit, 8, 5).
hard_strategy(hit, 9, 5).
hard_strategy(hit, 10, 5).
hard_strategy(hit, 11, 5).
hard_strategy(stand, 12, 5).
hard_strategy(stand, 13, 5).
hard_strategy(stand, 14, 5).
hard_strategy(stand, 15, 5).
hard_strategy(stand, 16, 5).
hard_strategy(stand, 17, 5).
hard_strategy(stand, 18, 5).
hard_strategy(stand, 19, 5).
hard_strategy(stand, 20, 5).

% dealer has 6, stand at 12
hard_strategy(hit, 4, 6).
hard_strategy(hit, 5, 6).
hard_strategy(hit, 6, 6).
hard_strategy(hit, 7, 6).
hard_strategy(hit, 8, 6).
hard_strategy(hit, 9, 6).
hard_strategy(hit, 10, 6).
hard_strategy(hit, 11, 6).
hard_strategy(stand, 12, 6).
hard_strategy(stand, 13, 6).
hard_strategy(stand, 14, 6).
hard_strategy(stand, 15, 6).
hard_strategy(stand, 16, 6).
hard_strategy(stand, 17, 6).
hard_strategy(stand, 18, 6).
hard_strategy(stand, 19, 6).
hard_strategy(stand, 20, 6).

% dealer has 7, stand at 17
hard_strategy(hit, 4, 7).
hard_strategy(hit, 5, 7).
hard_strategy(hit, 6, 7).
hard_strategy(hit, 7, 7).
hard_strategy(hit, 8, 7).
hard_strategy(hit, 9, 7).
hard_strategy(hit, 10, 7).
hard_strategy(hit, 11, 7).
hard_strategy(hit, 12, 7).
hard_strategy(hit, 13, 7).
hard_strategy(hit, 14, 7).
hard_strategy(hit, 15, 7).
hard_strategy(hit, 16, 7).
hard_strategy(stand, 17, 7).
hard_strategy(stand, 18, 7).
hard_strategy(stand, 19, 7).
hard_strategy(stand, 20, 7).

% dealer has 8, stand at 17
hard_strategy(hit, 4, 8).
hard_strategy(hit, 5, 8).
hard_strategy(hit, 6, 8).
hard_strategy(hit, 7, 8).
hard_strategy(hit, 8, 8).
hard_strategy(hit, 9, 8).
hard_strategy(hit, 10, 8).
hard_strategy(hit, 11, 8).
hard_strategy(hit, 12, 8).
hard_strategy(hit, 13, 8).
hard_strategy(hit, 14, 8).
hard_strategy(hit, 15, 8).
hard_strategy(hit, 16, 8).
hard_strategy(stand, 17, 8).
hard_strategy(stand, 18, 8).
hard_strategy(stand, 19, 8).
hard_strategy(stand, 20, 8).

% dealer has 9, stand at 17
hard_strategy(hit, 4, 9).
hard_strategy(hit, 5, 9).
hard_strategy(hit, 6, 9).
hard_strategy(hit, 7, 9).
hard_strategy(hit, 8, 9).
hard_strategy(hit, 9, 9).
hard_strategy(hit, 10, 9).
hard_strategy(hit, 11, 9).
hard_strategy(hit, 12, 9).
hard_strategy(hit, 13, 9).
hard_strategy(hit, 14, 9).
hard_strategy(hit, 15, 9).
hard_strategy(hit, 16, 9).
hard_strategy(stand, 17, 9).
hard_strategy(stand, 18, 9).
hard_strategy(stand, 19, 9).
hard_strategy(stand, 20, 9).

% dealer has 10, stand at 17
hard_strategy(hit, 4, 10).
hard_strategy(hit, 5, 10).
hard_strategy(hit, 6, 10).
hard_strategy(hit, 7, 10).
hard_strategy(hit, 8, 10).
hard_strategy(hit, 9, 10).
hard_strategy(hit, 10, 10).
hard_strategy(hit, 11, 10).
hard_strategy(hit, 12, 10).
hard_strategy(hit, 13, 10).
hard_strategy(hit, 14, 10).
hard_strategy(hit, 15, 10).
hard_strategy(hit, 16, 10).
hard_strategy(stand, 17, 10).
hard_strategy(stand, 18, 10).
hard_strategy(stand, 19, 10).
hard_strategy(stand, 20, 10).

% dealer has ace, stand at 17
hard_strategy(hit, 4, ace).
hard_strategy(hit, 5, ace).
hard_strategy(hit, 6, ace).
hard_strategy(hit, 7, ace).
hard_strategy(hit, 8, ace).
hard_strategy(hit, 9, ace).
hard_strategy(hit, 10, ace).
hard_strategy(hit, 11, ace).
hard_strategy(hit, 12, ace).
hard_strategy(hit, 13, ace).
hard_strategy(hit, 14, ace).
hard_strategy(hit, 15, ace).
hard_strategy(hit, 16, ace).
hard_strategy(stand, 17, ace).
hard_strategy(stand, 18, ace).
hard_strategy(stand, 19, ace).
hard_strategy(stand, 20, ace).

% soft total strategy
% strategy(Do this if, if score is, dealer has)
% Strategy is the strategy to use, this is an output
% Score is the score of the player's hand
% DealerScore is the score of the dealer's hand

% soft strats always deduct 11 from the score, then use the hard total strategy. this is why we only define the strats up to 11.

% easier and more overpowered than hard total strategy. you can literally play dumb and still win. we can hit even higher than 17 because we have an ace, hence, if we screwed up the 11 becomes 1.
% dealer has 2
soft_strategy(hit, 2, 2).
soft_strategy(hit, 3, 2).
soft_strategy(hit, 4, 2).
soft_strategy(hit, 5, 2).
soft_strategy(hit, 6, 2).
soft_strategy(stand, 7, 2). % stand at 7 because we have an ace. dealer busts at 17. if the dealer wins then we are just unlucky.
soft_strategy(stand, 8, 2).
soft_strategy(stand, 9, 2).
% no need. if you have 10 and an ace, you've already won. The Python end forbades you from hitting if you have 21 already.
soft_strategy(hit, 11, 2). % congratulations. your ace became 1. you can hit again.

% dealer has 3
soft_strategy(hit, 2, 3).
soft_strategy(hit, 3, 3).
soft_strategy(hit, 4, 3).
soft_strategy(hit, 5, 3).
soft_strategy(hit, 6, 3).
soft_strategy(stand, 7, 3).
soft_strategy(stand, 8, 3).
soft_strategy(stand, 9, 3).
soft_strategy(hit, 11, 3).

% dealer has 4
soft_strategy(hit, 2, 4).
soft_strategy(hit, 3, 4).
soft_strategy(hit, 4, 4).
soft_strategy(hit, 5, 4).
soft_strategy(hit, 6, 4).
soft_strategy(stand, 7, 4).
soft_strategy(stand, 8, 4).
soft_strategy(stand, 9, 4).
soft_strategy(hit, 11, 4).

% dealer has 5
soft_strategy(hit, 2, 5).
soft_strategy(hit, 3, 5).
soft_strategy(hit, 4, 5).
soft_strategy(hit, 5, 5).
soft_strategy(hit, 6, 5).
soft_strategy(stand, 7, 5).
soft_strategy(stand, 8, 5).
soft_strategy(stand, 9, 5).
soft_strategy(hit, 11, 5).

% dealer has 6
soft_strategy(hit, 2, 6).
soft_strategy(hit, 3, 6).
soft_strategy(hit, 4, 6).
soft_strategy(hit, 5, 6).
soft_strategy(hit, 6, 6).
soft_strategy(stand, 7, 6).
soft_strategy(stand, 8, 6).
soft_strategy(stand, 9, 6).
soft_strategy(hit, 11, 6).

% dealer has 7
soft_strategy(hit, 2, 7).
soft_strategy(hit, 3, 7).
soft_strategy(hit, 4, 7).
soft_strategy(hit, 5, 7).
soft_strategy(hit, 6, 7).
soft_strategy(stand, 7, 7).
soft_strategy(stand, 8, 7).
soft_strategy(stand, 9, 7).
soft_strategy(hit, 11, 7).

% dealer has 8
soft_strategy(hit, 2, 8).
soft_strategy(hit, 3, 8).
soft_strategy(hit, 4, 8).
soft_strategy(hit, 5, 8).
soft_strategy(hit, 6, 8).
soft_strategy(stand, 7, 8).
soft_strategy(stand, 8, 8).
soft_strategy(stand, 9, 8).
soft_strategy(hit, 11, 8).

% dealer has 9
soft_strategy(hit, 2, 9).
soft_strategy(hit, 3, 9).
soft_strategy(hit, 4, 9).
soft_strategy(hit, 5, 9).
soft_strategy(hit, 6, 9).
soft_strategy(hit, 7, 9).
soft_strategy(stand, 8, 9).
soft_strategy(stand, 9, 9).
soft_strategy(hit, 11, 9).

% dealer has 10
soft_strategy(hit, 2, 10).
soft_strategy(hit, 3, 10).
soft_strategy(hit, 4, 10).
soft_strategy(hit, 5, 10).
soft_strategy(hit, 6, 10).
soft_strategy(hit, 7, 10).
soft_strategy(stand, 8, 10).
soft_strategy(stand, 9, 10).
soft_strategy(hit, 11, 10).

% dealer has ace
soft_strategy(hit, 2, ace).
soft_strategy(hit, 3, ace).
soft_strategy(hit, 4, ace).
soft_strategy(hit, 5, ace).
soft_strategy(hit, 6, ace).
soft_strategy(hit, 7, ace).
soft_strategy(stand, 8, ace).
soft_strategy(stand, 9, ace).
soft_strategy(hit, 11, ace).

% deck memory play
% basically thinks what cards are left in the deck and plays accordingly. might even hit at 20 if the deck is full of low cards or stand at 12 if the deck is full of high cards.
% as known in the field of computing as Monte Carlo simulation. Albeit a very simple one.
% Hell, even it is named after a casino!

% Strategy is the strategy to use
% DealerCard is the dealer's card
% PlayerHand is the player's hand
% Deck is the deck to use

% to call, use deck_memory_strategy(Strategy, Table, Deck).

deck_memory_strategy(Strategy, DealerCard, PlayerHand, Deck, Count) :- % call helper with initial HasAce of false
    % remove all cards on the table from the deck
    subtract(Deck, DealerCard, TempDeck),
    subtract(TempDeck, PlayerHand, NewDeck),
    calculate_probability(NewDeck, Score, Count, TnB),

    % if the probability of busting (TnB/Count) is greater than 0.5, then hit. otherwise, stand.
    ( TnB/Count > 0.5 ->
        Strategy = hit;
        Strategy = stand ).

% calculate the probability of busting if the player were to hit
% Deck is the deck to use
% Score is the score used to calculate if the player will bust if the player were to hit
% Count is the number of times to calculate the probability
% TnB is the probability of not busting, this is an output

% to call, use calculate_probability(Deck, Score, Count, TnB).

calculate_probability(Deck, Score, Count, TnB) :- % call helper with initial TnB of 0
    calculate_probability(Deck, Score, Count, 0, TnB).

calculate_probability(Deck, Score, Count, TnB, TnB) :- % recursion base case: count is 0
    Count = 0.

calculate_probability(Deck, Score, Count, InTnB, TnB) :- % recursion BnB
    Count > 0,
    shuffle(Deck, TempDeck, 1), % shuffle the deck
    nth0(0, TempDeck, Card), % get the first card
    value(CardVal, Card), % get the value of the card
    % ace handling
    ( CardVal = 11 -> % if the card is an ace
        (Score + CardVal > 21 -> % and it it busts if we use ace as 11
            NewScore is Score + 1; % then use ace as 1
            NewScore is Score + CardVal); % otherwise use ace as 11
         NewScore is Score + CardVal ), % if the card is not an ace, then just add the value of the card to the score
    ( NewScore > 21 -> % if the score is greater than 21
        NewTnB is InTnB; % then do nothing to the counter, as the player has busted
        NewTnB is InTnB + 1 ), % the player has not busted, add 1 to the counter

    NewCount is Count - 1, % subtract 1 from the count
    calculate_probability(TempDeck, NewScore, NewCount, NewTnB, TnB).