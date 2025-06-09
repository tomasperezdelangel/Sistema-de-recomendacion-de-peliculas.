-- Filtros.hs
-- Módulo de filtrado de películas usando programación funcional

module Main where

import System.Environment
import Data.List (intercalate)

-- Definición del tipo de datos algebraico para películas
data Pelicula = Pelicula 
    { titulo :: String
    , genero :: String  
    , anio :: Int
    , rating :: Float
    } deriving (Show, Eq)

-- Función para crear una película desde una cadena CSV
parsePelicula :: String -> Pelicula
parsePelicula str = 
    let parts = splitOn ',' str
    in case parts of
        [t, g, a, r] -> Pelicula t g (read a) (read $ filter (/= '\r') r)
        _ -> error "Formato inválido de película"

-- Función auxiliar para dividir cadenas
splitOn :: Char -> String -> [String]
splitOn _ [] = []
splitOn c s = 
    let (before, remainder) = break (== c) s
    in before : case remainder of
                    [] -> []
                    (_:after) -> splitOn c after

-- Función de filtrado por género usando higher-order functions
filtrarPorGenero :: String -> [Pelicula] -> [Pelicula]
filtrarPorGenero generoFiltro = filter (\p -> genero p == generoFiltro)

-- Función de filtrado por año mínimo
filtrarPorAnio :: Int -> [Pelicula] -> [Pelicula]
filtrarPorAnio anioMinimo = filter (\p -> anio p >= anioMinimo)

-- Función de filtrado por rating mínimo
mejoresPeliculas :: Float -> [Pelicula] -> [Pelicula]
mejoresPeliculas ratingMinimo = filter (\p -> rating p >= ratingMinimo)

-- Función combinada de filtrado usando composición de funciones
filtrarPeliculas :: String -> Int -> Float -> [Pelicula] -> [Pelicula]
filtrarPeliculas gen anio_min rat_min = 
    filtrarPorGenero gen . filtrarPorAnio anio_min . mejoresPeliculas rat_min

-- Función para obtener géneros únicos usando fold
generosUnicos :: [Pelicula] -> [String]
generosUnicos = foldr (\p acc -> if genero p `elem` acc then acc else genero p : acc) []

-- Función para formatear películas como CSV
peliculaToCSV :: Pelicula -> String
peliculaToCSV p = intercalate "," [titulo p, genero p, show (anio p), show (rating p)]

-- Función principal que procesa argumentos de línea de comandos
main :: IO ()
main = do
    args <- getArgs
    case args of
        ["filtrar", generoArg, anioArg, ratingArg] -> do
            -- Leer películas desde stdin
            input <- getContents
            let peliculas = map parsePelicula (lines input)
            let peliculasFiltradas = filtrarPeliculas generoArg (read anioArg) (read ratingArg) peliculas
            -- Imprimir resultados
            mapM_ (putStrLn . peliculaToCSV) peliculasFiltradas
        ["generos"] -> do
            input <- getContents
            let peliculas = map parsePelicula (lines input)
            let generos = generosUnicos peliculas
            mapM_ putStrLn generos
        _ -> putStrLn "Uso: ./filtros filtrar <genero> <anio_min> <rating_min>"