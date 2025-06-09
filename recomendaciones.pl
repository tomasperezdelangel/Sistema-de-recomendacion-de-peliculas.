% recomendaciones.pl
% Sistema de recomendación de películas usando programación lógica

% Base de conocimiento - Hechos de películas
% pelicula(titulo, genero, anio, rating)
pelicula(interstellar, ciencia_ficcion, 2014, 8.6).
pelicula(blade_runner_2049, ciencia_ficcion, 2017, 8.0).
pelicula(the_matrix, ciencia_ficcion, 1999, 8.7).
pelicula(inception, ciencia_ficcion, 2010, 8.8).
pelicula(alien, ciencia_ficcion, 1979, 8.4).
pelicula(ex_machina, ciencia_ficcion, 2014, 7.7).

pelicula(the_godfather, drama, 1972, 9.2).
pelicula(forrest_gump, drama, 1994, 8.8).
pelicula(schindlers_list, drama, 1993, 8.9).
pelicula(the_shawshank_redemption, drama, 1994, 9.3).
pelicula(goodfellas, drama, 1990, 8.7).

pelicula(pulp_fiction, accion, 1994, 8.9).
pelicula(die_hard, accion, 1988, 8.2).
pelicula(mad_max_fury_road, accion, 2015, 8.1).
pelicula(john_wick, accion, 2014, 7.4).
pelicula(the_dark_knight, accion, 2008, 9.0).

pelicula(the_grand_budapest_hotel, comedia, 2014, 8.1).
pelicula(superbad, comedia, 2007, 7.6).
pelicula(anchorman, comedia, 2004, 7.2).
pelicula(the_big_lebowski, comedia, 1998, 8.1).

pelicula(the_conjuring, terror, 2013, 7.5).
pelicula(hereditary, terror, 2018, 7.3).
pelicula(get_out, terror, 2017, 7.7).
pelicula(the_witch, terror, 2015, 6.9).

% Reglas de recomendación básicas
% Recomendar películas con rating alto
recomendar_excelente(Pelicula) :-
    pelicula(Pelicula, _, _, Rating),
    Rating >= 8.5.

% Recomendar películas buenas
recomendar_buena(Pelicula) :-
    pelicula(Pelicula, _, _, Rating),
    Rating >= 7.5,
    Rating < 8.5.

% Recomendar por género específico
recomendar_por_genero(Pelicula, Genero) :-
    pelicula(Pelicula, Genero, _, _).

% Recomendar por género y rating minimo
recomendar_genero_rating(Pelicula, Genero, RatingMin) :-
    pelicula(Pelicula, Genero, _, Rating),
    Rating >= RatingMin.

% Recomendar películas modernas (después del 2010)
recomendar_moderna(Pelicula) :-
    pelicula(Pelicula, _, Anio, _),
    Anio >= 2010.

% Recomendar películas clásicas (antes del 2000)
recomendar_clasica(Pelicula) :-
    pelicula(Pelicula, _, Anio, _),
    Anio < 2000.

% Reglas de recomendación por perfil de usuario
% Para amantes de la ciencia ficción
perfil_sci_fi(Pelicula) :-
    pelicula(Pelicula, ciencia_ficcion, _, Rating),
    Rating >= 7.5, !.

% Para amantes del drama
perfil_drama(Pelicula) :-
    pelicula(Pelicula, drama, _, Rating),
    Rating >= 8.0, !.

% Para amantes de la acción
perfil_accion(Pelicula) :-
    pelicula(Pelicula, accion, _, Rating),
    Rating >= 7.5, !.

% Regla combinada: recomendar por multiples criterios
recomendar_completa(Pelicula, Genero, AnioMin, RatingMin) :-
    pelicula(Pelicula, Genero, Anio, Rating),
    Anio >= AnioMin,
    Rating >= RatingMin.

% Obtener informacion completa de una película
info_pelicula(Titulo, Genero, Anio, Rating) :-
    pelicula(Titulo, Genero, Anio, Rating).

% Encontrar la mejor película de un genero
mejor_del_genero(Pelicula, Genero, Rating) :-
    pelicula(Pelicula, Genero, _, Rating),
    \+ (pelicula(_, Genero, _, OtroRating), OtroRating > Rating).

% Contar películas por genero
contar_por_genero(Genero, Cantidad) :-
    findall(Pelicula, pelicula(Pelicula, Genero, _, _), Lista),
    length(Lista, Cantidad).

% Obtener todos los géneros disponibles
genero_disponible(Genero) :-
    pelicula(_, Genero, _, _).

% Predicado para obtener todas las peliculas de un genero ordenadas por rating
peliculas_ordenadas_por_rating(Genero, PeliculasOrdenadas) :-
    findall([Rating, Pelicula], pelicula(Pelicula, Genero, _, Rating), Lista),
    sort(Lista, ListaOrdenada),
    reverse(ListaOrdenada, PeliculasOrdenadas).

% Interfaz principal para consultas desde Python
consulta_principal(Tipo, Param1, Param2, Param3, Resultado) :-
    (   Tipo = 'recomendar_genero_rating' ->
        recomendar_genero_rating(Resultado, Param1, Param2)
    ;   Tipo = 'recomendar_completa' ->
        recomendar_completa(Resultado, Param1, Param2, Param3)
    ;   Tipo = 'info_pelicula' ->
        info_pelicula(Param1, Resultado, _, _)
    ;   Tipo = 'mejor_del_genero' ->
        mejor_del_genero(Resultado, Param1, _)
    ;   fail
    ).