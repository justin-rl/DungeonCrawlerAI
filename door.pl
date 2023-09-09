keysPossible(Input, Res) :- findall(Key, key(Input, Key), Res).

key(Input, first) :- first(Input).
key(Input, second) :- second(Input).
key(Input, third) :- third(Input).
key(Input, fourth) :- fourth(Input).
key(Input, sixth) :- sixth(Input).

first(Input) :-
   (member(gold, Input),
    member(red, Input),
    member(blue, Input),
    member(yellow, Input),
    \+ member(white, Input));

   (member(silver, Input),
    member(red, Input),
    member(blue, Input),
    \+ member(yellow, Input));

   (member(silver, Input),
    member(yellow, Input),
    member(red, Input),
    member(blue, Input),
    member(black, Input));

   (member(bronze, Input),
    member(red, Input),
    member(blue, Input),
    member(yellow, Input),
    member(black, Input)).

second(Input) :-
    (member(gold, Input),
     member(blue, Input),
     member(yellow, Input),
     \+ member(red, Input));

    (member(silver, Input),
     member(red, Input),
     member(blue, Input),
     member(yellow, Input),
     \+ member(black, Input));

    (member(bronze, Input),
     member(red, Input),
     member(blue, Input),
     member(yellow, Input),
     \+ member(black, Input)).

third(Input) :-
     member(bronze, Input),
     member(red, Input),
     member(blue, Input),
     member(black, Input),
     member(white, Input).

fourth(Input) :-
    member(gold, Input),
    member(red, Input),
    member(white, Input),
    member(blue, Input),
    member(yellow, Input),
    member(black, Input).

sixth(Input) :-
    member(bronze, Input),
    member(yellow, Input),
    member(white, Input),
    member(blue, Input),
    member(black, Input),
    member(white, Input).
