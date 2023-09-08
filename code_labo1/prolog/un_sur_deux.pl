appendop([], []).
appendop([F], [F]).
appendop([F,_|T], [F|X]) :- appendop(T, X).