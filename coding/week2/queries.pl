% ----- directors ------
movies_directed_by(DirName, Bag) :- findall(Movies,director_name(Movies,DirName), Bag).

common_director(X, Y):- director_name(X, D), director_name(Y, D), X \= Y.

% ----- genre ------
common_genre(X, Y) :- genre(X, G1), genre(Y, G1), X \= Y.

all_common_genre(X, Bag) :- findall(Movie, common_genre(X, Movie), Bag).

% ----- actors -----
actor_of(Movie, Actor) :- actor_1_name(Movie, Actor) ; actor_2_name(Movie, Actor) ; actor_3_name(Movie, Actor).

actors_of(Movie, Bag) :- findall(Actor, actor_of(Movie, Actor), Bag).

have_all_common_actors(Movie1, Movie2) :-
    common_actors_number(Movie1, Movie2, 3). 

have_some_common_actors(Movie1, Movie2) :-
    common_actors_number(Movie1, Movie2, X),
    X>=2.

have_more_than_one_common_actor(Movie1, Movie2) :-
    common_actors_number(Movie1, Movie2, X),
    X>=1.

common_actors(Movie1, Movie2, Actors) :-
    findall(A1, actor_of(Movie1, A1), Actors1), 
    findall(A2, actor_of(Movie2, A2), Actors2),
    intersection(Actors1, Actors2, Actors).

common_actors_number(Movie1, Movie2, Number) :-
    common_actors(Movie1, Movie2, Common),
    length(Common, Number).

% --- language ----

common_language(Movie1, Movie2):-
    language(Movie1, Lang),
    language(Movie2, Lang),
    Movie1 \= Movie2.

all_with_common_language(Movie1, Bag):-
    findall(Other, common_language(Movie1, Other), Bag).