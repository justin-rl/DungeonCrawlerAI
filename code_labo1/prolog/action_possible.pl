on(b, table).
on(a, table).
on(c, a).
clear(b).
clear(c).
block(a).
block(b).
block(c).

move(B, X, Y) :- clear(B), clear(Y), on(B,X), block(B), block(Y).
moveToTable(B, X) :- clear(B), on(B, X), block(B), block(X).

actionsPossibles([on(b, table), on(a, table), on(c, a), clear(b), clear(c), block(a), block(b), block(c)], R).