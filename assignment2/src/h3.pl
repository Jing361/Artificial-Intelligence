% Cities are:
%
% akron
% athens
% beavercreek
% cincinnati
% circleville
% columbus
% dayton
% newport
%

% set-up all flights
% set-up all flights from akron
fly(akron, athens, 6, 7).
fly(akron, beavercreek, 10, 11).
fly(akron, columbus, 8, 9).
fly(akron, dayton, 7, 8).
fly(akron, newport, 9, 10).

% set-up all flights from athens
fly(athens, akron, 14, 15).
fly(athens, beavercreek, 15, 16).
fly(athens, columbus, 13, 14).
fly(athens, dayton, 12, 13).
fly(athens, newport, 11, 12).

% set-up all flights from beavercreek
fly(beavercreek, cincinnati, 16, 17).
fly(beavercreek, columbus, 17, 18).
fly(beavercreek, dayton, 18, 19).
fly(beavercreek, newport, 19, 20).
fly(beavercreek, akron, 20, 21).

% set-up all flights from cincinnati
fly(cincinnati, akron, 23, 0).
fly(cincinnati, athens, 0, 1).
fly(cincinnati, cincinnati, 1, 2).
fly(cincinnati, circleville, 22, 23).
fly(cincinnati, columbus, 21, 22).

% set-up all flights from circleville
fly(circleville, athens, 4, 5).
fly(circleville, beavercreek, 5, 6).
fly(circleville, cincinnati, 6, 7).
fly(circleville, dayton, 3, 4).
fly(circleville, newport, 2, 3).

% set-up all flights from columbus
fly(columbus, circleville, 7, 8).
fly(columbus, dayton, 8, 9).
fly(columbus, cincinnati, 9, 10).
fly(columbus, athens, 10, 11).
fly(columbus, beavercreek, 11, 12).

% set-up all flights from dayton
fly(dayton, athens, 3, 4).
fly(dayton, cincinnati, 2, 3).
fly(dayton, circleville, 4, 5).
fly(dayton, columbus, 5, 6).
fly(dayton, newport, 1, 2).

% set-up all flights from newport
fly(newport, circleville, 12, 13).
fly(newport, akron, 13, 14).
fly(newport, beavercreek, 14, 15).
fly(newport, akron, 15, 16).
fly(newport, circleville, 16, 17).

% find a flight such that we leave after Start and reach before Stop.
fly(City1, City2, Start, Stop):-
    City1\=City2,
    fly(City1, MidCity, Y, Z),
    fly(MidCity, City2, W, R),
    Y>=Start,
    R=<Stop,
    W>=Z.

% flights can be found using connections, with no time restrictions.
fly(City1, City2):-
    City1\=City2,
    fly(City1, MidCity, Y, Z),
    fly(MidCity, City2, W, R).

