max(A, B, C) :-
    A>=B -> C is A; C is B.  

min(A, B, C) :-
    A>=B -> C is B; C is A.

% ----- directors ------
    have_common_director(X, Y) :-
        director_name(X, D),
        director_name(Y, D),
        X \= Y.

    all_with_common_director(Movie1, Movies) :-
        findall(Movie, common_director(Movie1, Movie), Movies).

% -------


% ----- genre ------

    /*
        genres_of(Movie, Genres) :-
            findall(Genre, genre(Movie, Genre), Genres).

        genres_num_of(Movie, Num) :-
            genres_of(Movie, Genres),
            length(Genres, Num).

        common_genres(Movie1, Movie2, Genres) :- 
            genres_of(Movie1, Genres1),
            genres_of(Movie2, Genres2),
            intersection(Genres1, Genres2, Genres).

        common_genres_number(Movie1, Movie2, Num) :-
            common_genres(Movie1, Movie2, Genres),
            length(Genres, Num).
    */

    % num of common genres = minL
    have_three_common_genres(Movie1, Movie2) :-
        Movie1 \= Movie2,
        genre(Movie1, G1),
        genre(Movie1, G2),
        genre(Movie1, G3),
        genre(Movie2, G1),
        genre(Movie2, G2),
        genre(Movie2, G3),
        G1 \= G2,
        G2 \= G3,
        G3 \= G1.

    % num of common genres >= min(2, minL)
    have_two_common_genres(Movie1, Movie2) :-
        genre(Movie1, G1),
        genre(Movie1, G2),
        genre(Movie2, G1),
        genre(Movie2, G2),
        Movie1 \= Movie2,
        G1 \= G2.

    have_one_common_genre(Movie1, Movie2) :-
        genre(Movie1, G1),
        genre(Movie2, G1),
        Movie1 \= Movie2.

    all_with_many_common_genres(Movie1, Movies) :-
        findall(Movie, have_three_common_genres(Movie1, Movie), Movies).

    all_with_some_common_genres(Movie1, Movies) :-
        findall(Movie, have_two_common_genres(Movie1, Movie), Movies).

    all_with_one_common_genre(Movie1, Movies) :-
        findall(Movie, have_one_common_genre(Movie1, Movie), Movies).
% -------


% ----- actors -----

    actor_of(Movie, Actor) :-
        actor_1_name(Movie, Actor) ; actor_2_name(Movie, Actor) ; actor_3_name(Movie, Actor).


    /*
        actors_of(Movie, Actors) :-
            findall(Actor, actor_of(Movie, Actor), Actors).

        common_actors(Movie1, Movie2, Actors) :-
            actors_of(Movie1, Actors1), 
            actors_of(Movie2, Actors2),
            intersection(Actors1, Actors2, Actors).

        common_actors_number(Movie1, Movie2, Number) :-
            common_actors(Movie1, Movie2, Common),
            length(Common, Number).
    */

    have_all_common_actors(Movie1, Movie2) :-
        Movie1 \= Movie2,
        actor_1_name(Movie1, Actor1),
        actor_2_name(Movie1, Actor2),
        actor_3_name(Movie1, Actor3),
        actor_of(Movie2, Actor1),
        actor_of(Movie2, Actor2),
        actor_of(Movie2, Actor3).
        
    have_some_common_actors(Movie1, Movie2) :-
        actor_1_name(Movie1, Actor1),
        actor_2_name(Movie1, Actor2),
        actor_3_name(Movie1, Actor3),
        Movie1 \= Movie2,
        (actor_of(Movie2, Actor1),actor_of(Movie2, Actor2));
        (actor_of(Movie2, Actor1),actor_of(Movie2, Actor3));
        (actor_of(Movie2, Actor2),actor_of(Movie2, Actor3)).

    have_one_common_actor(Movie1, Movie2) :-
        actor_of(Movie1, Actor),
        actor_of(Movie2, Actor),
        Movie1 \= Movie2.

    all_with_all_common_actors(Movie1, Movies) :-
        findall(Movie, have_all_common_actors(Movie1, Movie), Movies).

    all_with_some_common_actors(Movie1, Movies) :-
        setof(Movie, have_some_common_actors(Movie1, Movie), Movies).

    all_with_one_common_actor(Movie1, Movies) :-
        findall(Movie, have_one_common_actor(Movie1, Movie), Movies).

% -----


% --- plot keywords ----

    /*
        keywords_of(Movie, Keywords) :-
            findall(Word, plot_keyword(Movie, Word), Keywords).

        keywords_num_of(Movie, Num) :-
            keywords_of(Movie, Words),
            length(Words, Num).

        common_keywords(Movie1, Movie2, Words) :-
            keywords_of(Movie1, Words1),
            keywords_of(Movie2, Words2),
            intersection(Words1, Words2, Words).

        common_keywords_number(Movie1, Movie2, Num) :-
            common_keywords(Movie1, Movie2, Common),
            length(Common, Num).
    */

    have_three_common_keywords(Movie1, Movie2) :-
        plot_keyword(Movie1, Word1),
        plot_keyword(Movie1, Word2),
        plot_keyword(Movie1, Word3),
        plot_keyword(Movie2, Word1),
        plot_keyword(Movie2, Word2),
        plot_keyword(Movie2, Word3),
        Movie1 \= Movie2,
        Word1 \= Word2,
        Word2 \= Word3,
        Word1 \= Word3.

    have_two_common_keywords(Movie1, Movie2) :-
        plot_keyword(Movie1, Word1),
        plot_keyword(Movie1, Word2),
        plot_keyword(Movie2, Word1),
        plot_keyword(Movie2, Word2),
        Movie1 \= Movie2,
        Word1 \= Word2.

    have_one_common_keyword(Movie1, Movie2):-
        plot_keyword(Movie1, Word),
        plot_keyword(Movie2, Word),
        Movie1 \= Movie2.

    all_with_three_common_keywords(Movie1, Movies) :-
        findall(Movie, have_three_common_keywords(Movie1, Movie), Movies).

    all_with_two_common_keywords(Movie1, Movies) :-
        findall(Moviee, have_two_common_keywords(Movie1, Moviee), Movies).

    all_with_one_common_keyword(Movie1, Movies) :-
        findall(Movie, have_one_common_keyword(Movie1, Movie), Movies).

% -------------


% --- production_country ----
    have_same_production_country(Movie1, Movie2) :-
        production_country(Movie1, Country),
        production_country(Movie2, Country),
        Movie1 \= Movie2.

    all_with_same_production_country(Movie1, Movies) :-
        findall(Movie, have_same_production_country(Movie1, Movie), Movies).
% -----------------

% --- country -----
    have_same_country(Movie1, Movie2) :-
        country(Movie1, Country),
        country(Movie2, Country),
        Movie1 \= Movie2.

    all_with_same_country(Movie1, Movies) :-
        findall(Movie, have_same_country(Movie1, Movie), Movies).
% -------------

% --- company ---- 
    have_same_company(Movie1, Movie2) :-
        production_company(Movie1, Company),
        production_company(Movie2, Company),
        Movie1 \= Movie2.
% ---------------

% --- budget ----
    have_close_budget(Movie1, Movie2) :-
        budget(Movie1, Budget1),
        budget(Movie2, Budget2),
        Movie1 \= Movie2,
        number_string(B1, Budget1),
        number_string(B2, Budget2),           
        0.5 * B1 < B2,
        B2 < 2 * B1.

    all_with_close_budget(Movie1, Movies) :-
        findall(Movie, have_close_budget(Movie1, Movie), Movies).
% -------

% --- popularity ----
    have_close_popularity(Movie1, Movie2) :-
        popularity(Movie1, Popularity1),
        popularity(Movie2, Popularity2),
        Movie1 \= Movie2,
        number_string(Pop1, Popularity1),
        number_string(Pop2, Popularity2),
        0.9 * Pop1 < Pop2,
        Pop2 < 1.1 * Pop1.
    
    all_with_close_popularity(Movie1, Movies) :-
        findall(Movie, have_close_popularity(Movie, Movie1), Movies).

% ------------

% --- release date ----
    release_year(Movie1, Year) :-
        release_date(Movie1, Date1),
        split_string(Date1, "-", "", Parts),
        nth0(0, Parts, Year).

    release_decade(Movie1, Dec) :-
        release_year(Movie1, Year),
        once(sub_string(Year, _, 3, _, Decade)),
        number_string(Dec, Decade).

    have_same_release_year(Movie1, Movie2) :-
        release_year(Movie1, Year),
        release_year(Movie2, Year),
        Movie1 \= Movie2.

    have_same_release_decade(Movie1, Movie2) :-
        release_decade(Movie1, Dec),
        release_decade(Movie2, Dec),
        Movie1 \= Movie2.

    all_with_same_release_year(Movie1, Movies) :-
        findall(Movie, have_same_release_year(Movie1, Movie), Movies).

    all_with_same_release_decade(Movie1, Movies) :-
        findall(Movie, have_same_release_decade(Movie1, Movie), Movies).

% -------

% --- gross ----
    have_close_gross(Movie1, Movie2) :-
        gross(Movie1, Gross1),
        gross(Movie2, Gross2),
        Movie1 \= Movie2,
        number_string(G1, Gross1),
        number_string(G2, Gross2),
        0.9 * G1 < G2,
        G2 < 1.1 * G1.
    
    all_with_close_gross(Movie1, Movies) :-
        findall(Movie, have_close_gross(Movie, Movie1), Movies).

% ------------

% --- language ----
    have_common_language(Movie1, Movie2):-
        language(Movie1, Lang),
        language(Movie2, Lang),
        Movie1 \= Movie2.

    all_with_common_language(Movie1, Bag):-
        findall(Other, common_language(Movie1, Other), Bag).

% --------

% --- spoken_languages ----

    have_common_spoken_language(Movie1, Movie2) :-
        spoken_languages(Movie1, Lang1),
        spoken_languages(Movie2, Lang1),
        Movie1 \= Movie2.

    all_with_common_spoken_language(Movie1, Movies) :-
        findall(Movie, have_common_spoken_language(Movie1, Movie), Movies).

% --------

% --- status ----
    have_same_status(Movie1, Movie2) :-
        status(Movie1, Status1),
        status(Movie2, Status1),
        Movie1 \=Movie2.

% --------

% --- movie_title ----

    have_close_title(Movie1, Movie2) :-
        sub_string(Movie1, _, 7, _, Sub1),
        sub_string(Movie2, _, 7, _, Sub1),
        not(sub_string(Sub1, _, _, _, 'and')),
        not(sub_string(Sub1, _, _, _, 'ing')),
        not(sub_string(Sub1, _, _, _, 'of')),
        not(sub_string(Sub1, _, _, _, 'the')),

        Movie1 \= Movie2.

    all_with_close_title(Movie1, Movies) :-
        setof(Movie, have_close_title(Movie1, Movie), Movies).

% --------

% --- tagline ----

    have_close_tagline(Movie1, Movie2) :-
        tagline(Movie1, Title1),
        tagline(Movie2, Title2),
        sub_string(Title1, _, 5, _, Sub1),
        sub_string(Title2, _, 5, _, Sub1),
        not(sub_string(Sub1, _, _, _, 'and')),
        not(sub_string(Sub1, _, _, _, 'ing')),
        Movie1 \= Movie2.

    all_with_close_tagline(Movie1, Movies) :-
        setof(Movie, have_close_tagline(Movie1, Movie), Movies).

% --------

% --- vote_average  (bearing in mind the num_voted_users) ----

    have_close_vote_average(Movie1, Movie2) :-
        vote_average(Movie1, Average1),
        vote_average(Movie2, Average2),
        number_string(Av1, Average1),
        number_string(Av2, Average2),
        %num_voted_users(Movie1, Users1),
        %num_voted_users(Movie2, Users2),
        %number_string(Us1, Users1),
        %number_string(Us2, Users2),      
        0.95*Av1 =< Av2, Av2 =< 1.15*Av1,
        %0.5*Us1 =< Us2,
        Movie1 \= Movie2.    

    all_with_close_vote_average(Movie1, Movies) :-
        findall(Movie, have_close_vote_average(Movie1, Movie), Movies).

% --------

% --- duration -----
    have_close_duration(Movie1, Movie2) :-
        duration(Movie1, Duration1),
        duration(Movie2, Duration2),
        number_string(Dur1, Duration1),
        number_string(Dur2, Duration2),
        0.95*Dur1 =< Dur2, Dur2 =< 1.15*Dur1,
        Movie1 \= Movie2.

    all_with_close_duration(Movie1, Movies) :-
        findall(Movie, have_close_duration(Movie1, Movie), Movies).
% --------