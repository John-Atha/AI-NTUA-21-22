% for Avatar

have_high_votes(Y) :-
    vote_average(Y, V),
    number_string(Vnum, V),
    Vnum >= 7.

have_close_keywords_genres(X, Y) :-
    have_two_common_keywords(X, Y);
    have_two_common_genres(X, Y).

have_close_director_actor(X, Y) :-
    have_common_director(X, Y);
    have_one_common_actor(X, Y).


have_close_languages(X, Y) :-
    have_common_spoken_language(X, Y);
    have_common_language(X, Y).

have_close_countries(X, Y) :-
    have_same_country(X, Y);
    have_same_production_country(X, Y).

have_same_people_or_high_votes(X, Y) :-
    have_common_director(X, Y);
    have_one_common_actor(X, Y);
    have_high_votes(Y).

% finds around 100-150 recommendations
find_sim_1(X, Y) :-
    have_close_keywords_genres(X, Y),
    have_same_people_or_high_votes(X, Y);
    X \= Y.

% finds around 60-70 recommendations
find_sim_2(X, Y) :-
    find_sim_1(X, Y),
    (
        have_close_duration(X, Y);
        have_same_company(X, Y);
        have_same_release_decade(X, Y)
    ).

% finds around 30-60 recommendations
find_sim_3(X, Y) :-
    (
        (
            have_two_common_genres(X, Y),
            have_close_title(X, Y)
        );
        (
            (
                have_one_common_genre(X, Y),
                have_one_common_keyword(X, Y)
            ),
            have_same_people_or_high_votes(X, Y)
        )
    ),
    X \= Y.

% finds around 10 recommendations
find_sim_4(X, Y) :-
    (   
        (
            have_two_common_genres(X, Y),
            have_close_title(X, Y)
        );

        (
            have_two_common_genres(X, Y),
            have_one_common_keyword(X, Y),
            have_same_people_or_high_votes(X, Y),
            have_close_budget(X, Y)
        )
    ),
    X \= Y.

find_sim_5(X, Y) :-
    (
        (
            have_two_common_genres(X, Y),
            have_close_title(X, Y)
        );
        (
            (
                have_two_common_genres(X, Y),
                have_two_common_keywords(X, Y)
            ),
            have_close_director_actor(X, Y),
            have_close_languages(X, Y),
            have_close_countries(X, Y)
        )
    ),
    X \= Y.