keysPossible(Input, Res) :- delete(Input, '', X), findall(Key, key(X, Key), Res).

key(Input, first) :- first(Input).
key(Input, second) :- second(Input).
key(Input, third) :- third(Input).
key(Input, fourth) :- fourth(Input).
key(Input, sixth) :- sixth(Input).

count_item(_, [], 0).
count_item(X, [X | T], N) :- !, count_item(X, T, N1), N is N1 + 1.
count_item(X, [_ | T], N) :- count_item(X, T, N).

indexOf([Element|_], Element, 0).
indexOf([_|Tail], Element, Index) :-
   indexOf(Tail, Element, Index1), Index is Index1 + 1.

%rules for 3 crystals:
second(Input) :- length(Input, 4), \+ member(red, Input).
third(Input) :- length(Input, 4), member(red, Input), last(Input, white).
second(Input) :- length(Input, 4), member(red, Input), \+ last(Input, white), count_item(blue, Input, N), N>1, \+ last(Input, blue).
third(Input) :- length(Input, 4), member(red, Input), \+ last(Input, white), count_item(blue, Input, N), N>1, last(Input, blue).
first(Input) :- length(Input, 4), member(red, Input), \+ last(Input, white), count_item(blue, Input, N), N = 1.

%rules for 4 crystals:
second(Input) :- length(Input, 5), member(silver, Input), count_item(red, Input, N), N>1,findall(Index, indexOf(Input, red, Index), X), last(X,2).
third(Input) :- length(Input, 5), member(silver, Input), count_item(red, Input, N), N>1, findall(Index, indexOf(Input, red, Index), X), last(X,3).
fourth(Input) :- length(Input, 5), member(silver, Input), count_item(red, Input, N), N>1, findall(Index, indexOf(Input, red, Index), X), last(X,4).
first(Input) :- length(Input, 5), \+ member(red, Input), last(Input, yellow).
first(Input) :- length(Input, 5), \+member(silver, Input), count_item(blue, Input, N), N=1, member(red, Input).
fourth(Input) :- length(Input, 5), count_item(yellow, Input, N), N>1, not((count_item('blue', Input, I), I=1)), member(red, Input).
second(Input) :- length(Input, 5), count_item(yellow, Input, N), N=<1, not((count_item('blue', Input, I), I=1)), member(red, Input).

%rules for 5 crystals:
fourth(Input) :- length(Input, 6), last(Input, black), member(gold, Input).
first(Input) :- length(Input, 6), not((last(Input, black), member(gold, Input))), count_item(red, Input, N), N=1, count_item(yellow, Input, I), I>1.
second(Input) :- length(Input, 6), not((count_item(red, Input, N), N=1, count_item(yellow, Input, I), I>1)), \+ member(black, Input).
first(Input) :- length(Input, 6), not((count_item(red, Input, N), N=1, count_item(yellow, Input, I), I>1)), member(black, Input).

%rules for 6 crystals:
third(Input) :- length(Input, 7), \+ member(yellow, Input), member(bronze, Input).
fourth(Input) :- length(Input, 7), count_item(yellow, Input, N), N=1, count_item(white, Input, I), I>1.
sixth(Input) :- length(Input, 7), not((count_item(yellow, Input, N), N=1, count_item(white, Input, I), I>1)), \+ member(red, Input).
fourth(Input) :- length(Input, 7), not((count_item(yellow, Input, N), N=1, count_item(white, Input, I), I>1)), member(red, Input).

