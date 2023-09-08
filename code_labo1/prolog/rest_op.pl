hors_oeuvre(salad).
hors_oeuvre(pate).
poisson(sole).
poisson(thon).
viande(porc).
viande(boeuf).
dessert(glace).
dessert(fruit).

plat(X) :- poisson(X) ; viande(X).

points(1, salad).
points(6, pate).
points(2, sole).
points(4, thon).
points(7, porc).
points(3, boeuf).
points(5, glace).
points(1, fruit).

score(H, P, D, S) :- points(X, H), points(Y, P), points(Z, D), S is X + Y + Z.

islege(S) :- S >= 10.

repas(H, P, D) :- hors_oeuvre(H), plat(P), dessert(D), score(H, P, D, S), islege(S).
repaslege(H, P, D) :- hors_oeuvre(H), plat(P), dessert(D), score(H, P, D, S), 10 > S.