keysPossible(Input, Res) :- findall(Key, key(Input, Key), Res).

key(Input, first) :- first(Input).
key(Input, second) :- second(Input).
key(Input, third) :- third(Input).

list_length([], 0).
list_length([_|Tail], N) :- list_length(Tail, N1), N is N1 + 1.

count_item(_, [], 0).
count_item(X, [X | T], N) :- !, count(X, T, N1), N is N1 + 1.
count_item(X, [_ | T], N) :- count(X, T, N).

second(Input) :- length(Input, 4), \+ member(red, Input).
third(Input) :- member(red, Input), last(Input, white).
first(Input) :- length(Input, 4), member(red, Input), \+ last(Input, white), count_item(blue, Input, N), N = 1.

