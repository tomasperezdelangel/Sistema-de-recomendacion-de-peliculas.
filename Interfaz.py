#!/usr/bin/env python3
"""
Sistema de Recomendación de Películas
Integra Haskell (filtrado) y Prolog (recomendaciones) con interfaz gráfica
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import subprocess
import tempfile
import os
from pyswip import Prolog

class SistemaRecomendacion:
    def __init__(self):
        # Datos de películas para Haskell
        self.peliculas_csv = [
            "Interstellar,ciencia_ficcion,2014,8.6",
            "Blade Runner 2049,ciencia_ficcion,2017,8.0",
            "The Matrix,ciencia_ficcion,1999,8.7",
            "Inception,ciencia_ficcion,2010,8.8",
            "Alien,ciencia_ficcion,1979,8.4",
            "Ex Machina,ciencia_ficcion,2014,7.7",
            "The Godfather,drama,1972,9.2",
            "Forrest Gump,drama,1994,8.8",
            "Schindler's List,drama,1993,8.9",
            "The Shawshank Redemption,drama,1994,9.3",
            "Goodfellas,drama,1990,8.7",
            "Pulp Fiction,accion,1994,8.9",
            "Die Hard,accion,1988,8.2",
            "Mad Max Fury Road,accion,2015,8.1",
            "John Wick,accion,2014,7.4",
            "The Dark Knight,accion,2008,9.0",
            "The Grand Budapest Hotel,comedia,2014,8.1",
            "Superbad,comedia,2007,7.6",
            "Anchorman,comedia,2004,7.2",
            "The Big Lebowski,comedia,1998,8.1",
            "The Conjuring,terror,2013,7.5",
            "Hereditary,terror,2018,7.3",
            "Get Out,terror,2017,7.7",
            "The Witch,terror,2015,6.9"
        ]
        
        # Inicializar Prolog
        try:
            self.prolog = Prolog()
            # Aquí cargarías el archivo recomendaciones.pl
            # self.prolog.consult("recomendaciones.pl")
            self.setup_prolog_facts()
        except Exception as e:
            print(f"Error inicializando Prolog: {e}")
            self.prolog = None
        
        self.setup_gui()
    
    def setup_prolog_facts(self):
        """Configura los hechos de Prolog directamente"""
        if not self.prolog:
            return
            
        # Definir hechos de películas
        peliculas_prolog = [
            ("interstellar", "ciencia_ficcion", 2014, 8.6),
            ("blade_runner_2049", "ciencia_ficcion", 2017, 8.0),
            ("the_matrix", "ciencia_ficcion", 1999, 8.7),
            ("inception", "ciencia_ficcion", 2010, 8.8),
            ("alien", "ciencia_ficcion", 1979, 8.4),
            ("ex_machina", "ciencia_ficcion", 2014, 7.7),
            ("the_godfather", "drama", 1972, 9.2),
            ("forrest_gump", "drama", 1994, 8.8),
            ("schindlers_list", "drama", 1993, 8.9),
            ("the_shawshank_redemption", "drama", 1994, 9.3),
            ("goodfellas", "drama", 1990, 8.7),
            ("pulp_fiction", "accion", 1994, 8.9),
            ("die_hard", "accion", 1988, 8.2),
            ("mad_max_fury_road", "accion", 2015, 8.1),
            ("john_wick", "accion", 2014, 7.4),
            ("the_dark_knight", "accion", 2008, 9.0),
            ("the_grand_budapest_hotel", "comedia", 2014, 8.1),
            ("superbad", "comedia", 2007, 7.6),
            ("anchorman", "comedia", 2004, 7.2),
            ("the_big_lebowski", "comedia", 1998, 8.1),
            ("the_conjuring", "terror", 2013, 7.5),
            ("hereditary", "terror", 2018, 7.3),
            ("get_out", "terror", 2017, 7.7),
            ("the_witch", "terror", 2015, 6.9)
        ]
        
        # Asegurar que las reglas están disponibles
        try:
            for titulo, genero, anio, rating in peliculas_prolog:
                self.prolog.assertz(f"pelicula({titulo}, {genero}, {anio}, {rating})")
            
            # Definir reglas básicas
            self.prolog.assertz("recomendar_excelente(Pelicula) :- pelicula(Pelicula, _, _, Rating), Rating >= 8.5")
            self.prolog.assertz("recomendar_buena(Pelicula) :- pelicula(Pelicula, _, _, Rating), Rating >= 7.5, Rating < 8.5")
            self.prolog.assertz("recomendar_por_genero(Pelicula, Genero) :- pelicula(Pelicula, Genero, _, _)")
            self.prolog.assertz("recomendar_genero_rating(Pelicula, Genero, RatingMin) :- pelicula(Pelicula, Genero, _, Rating), Rating >= RatingMin")
            self.prolog.assertz("recomendar_completa(Pelicula, Genero, AnioMin, RatingMin) :- pelicula(Pelicula, Genero, Anio, Rating), Anio >= AnioMin, Rating >= RatingMin")
            
        except Exception as e:
            print(f"Error configurando hechos Prolog: {e}")
    
    def setup_gui(self):
        """Configura la interfaz gráfica"""
        self.root = tk.Tk()
        self.root.title("Sistema de Recomendación de Películas")
        self.root.geometry("800x600")
        
        # Crear notebook para pestañas
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Pestaña de filtrado Haskell
        self.frame_haskell = ttk.Frame(notebook)
        notebook.add(self.frame_haskell, text="Filtrado (Haskell)")
        self.setup_haskell_tab()
        
        # Pestaña de recomendaciones Prolog
        self.frame_prolog = ttk.Frame(notebook)
        notebook.add(self.frame_prolog, text="Recomendaciones (Prolog)")
        self.setup_prolog_tab()
        
        # Pestaña de información
        self.frame_info = ttk.Frame(notebook)
        notebook.add(self.frame_info, text="Base de Datos")
        self.setup_info_tab()
    
    def setup_haskell_tab(self):
        """Configura la pestaña de filtrado con Haskell"""
        # Título
        ttk.Label(self.frame_haskell, text="Filtrado de Películas (Haskell)", 
                 font=('Arial', 14, 'bold')).pack(pady=10)
        
        # Frame para controles
        controls_frame = ttk.Frame(self.frame_haskell)
        controls_frame.pack(fill='x', padx=20, pady=10)
        
        # Género
        ttk.Label(controls_frame, text="Género:").grid(row=0, column=0, sticky='w', padx=5)
        self.genero_var = tk.StringVar(value="ciencia_ficcion")
        genero_combo = ttk.Combobox(controls_frame, textvariable=self.genero_var, 
                                   values=["ciencia_ficcion", "drama", "accion", "comedia", "terror"])
        genero_combo.grid(row=0, column=1, padx=5, sticky='ew')
        
        # Año mínimo
        ttk.Label(controls_frame, text="Año mínimo:").grid(row=1, column=0, sticky='w', padx=5)
        self.anio_var = tk.StringVar(value="2000")
        ttk.Entry(controls_frame, textvariable=self.anio_var).grid(row=1, column=1, padx=5, sticky='ew')
        
        # Rating mínimo
        ttk.Label(controls_frame, text="Rating mínimo:").grid(row=2, column=0, sticky='w', padx=5)
        self.rating_var = tk.StringVar(value="7.0")
        ttk.Entry(controls_frame, textvariable=self.rating_var).grid(row=2, column=1, padx=5, sticky='ew')
        
        # Botón filtrar
        ttk.Button(controls_frame, text="Filtrar", command=self.filtrar_haskell).grid(row=3, column=0, columnspan=2, pady=10)
        
        controls_frame.columnconfigure(1, weight=1)
        
        # Área de resultados
        ttk.Label(self.frame_haskell, text="Resultados:").pack(anchor='w', padx=20)
        self.resultado_haskell = scrolledtext.ScrolledText(self.frame_haskell, height=15)
        self.resultado_haskell.pack(fill='both', expand=True, padx=20, pady=10)
    
    def setup_prolog_tab(self):
        """Configura la pestaña de recomendaciones con Prolog"""
        # Título
        ttk.Label(self.frame_prolog, text="Recomendaciones (Prolog)", 
                 font=('Arial', 14, 'bold')).pack(pady=10)
        
        # Frame para controles
        controls_frame = ttk.Frame(self.frame_prolog)
        controls_frame.pack(fill='x', padx=20, pady=10)
        
        # Tipo de recomendación
        ttk.Label(controls_frame, text="Tipo de recomendación:").grid(row=0, column=0, sticky='w', padx=5)
        self.tipo_recom_var = tk.StringVar(value="recomendar_excelente")
        tipo_combo = ttk.Combobox(controls_frame, textvariable=self.tipo_recom_var, 
                                 values=["recomendar_excelente", "recomendar_buena", "recomendar_por_genero", "recomendar_genero_rating"])
        tipo_combo.grid(row=0, column=1, padx=5, sticky='ew')
        
        # Parámetros adicionales
        ttk.Label(controls_frame, text="Género (si aplica):").grid(row=1, column=0, sticky='w', padx=5)
        self.genero_prolog_var = tk.StringVar(value="ciencia_ficcion")
        ttk.Combobox(controls_frame, textvariable=self.genero_prolog_var,
                    values=["ciencia_ficcion", "drama", "accion", "comedia", "terror"]).grid(row=1, column=1, padx=5, sticky='ew')
        
        ttk.Label(controls_frame, text="Rating mínimo (si aplica):").grid(row=2, column=0, sticky='w', padx=5)
        self.rating_prolog_var = tk.StringVar(value="8.0")
        ttk.Entry(controls_frame, textvariable=self.rating_prolog_var).grid(row=2, column=1, padx=5, sticky='ew')
        
        # Botón recomendar
        ttk.Button(controls_frame, text="Recomendar", command=self.recomendar_prolog).grid(row=3, column=0, columnspan=2, pady=10)
        
        controls_frame.columnconfigure(1, weight=1)
        
        # Área de resultados
        ttk.Label(self.frame_prolog, text="Recomendaciones:").pack(anchor='w', padx=20)
        self.resultado_prolog = scrolledtext.ScrolledText(self.frame_prolog, height=15)
        self.resultado_prolog.pack(fill='both', expand=True, padx=20, pady=10)
    
    def setup_info_tab(self):
        """Configura la pestaña de información de la base de datos"""
        ttk.Label(self.frame_info, text="Base de Datos de Películas", 
                 font=('Arial', 14, 'bold')).pack(pady=10)
        
        # Mostrar todas las películas
        info_text = scrolledtext.ScrolledText(self.frame_info, height=25)
        info_text.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Agregar información de las películas
        info_content = "PELÍCULAS EN LA BASE DE DATOS:\n\n"
        info_content += "Formato: Título, Género, Año, Rating\n"
        info_content += "=" * 50 + "\n\n"
        
        for pelicula in self.peliculas_csv:
            info_content += pelicula + "\n"
        
        info_text.insert('1.0', info_content)
        info_text.config(state='disabled')
    
    def filtrar_haskell(self):
        """Ejecuta el filtrado usando Haskell (simulado)"""
        try:
            genero = self.genero_var.get()
            anio_min = int(self.anio_var.get())
            rating_min = float(self.rating_var.get())
            
            # Simulación del filtrado de Haskell
            resultados = []
            for pelicula_csv in self.peliculas_csv:
                partes = pelicula_csv.split(',')
                titulo, gen, anio, rating = partes[0], partes[1], int(partes[2]), float(partes[3])
                
                if gen == genero and anio >= anio_min and rating >= rating_min:
                    resultados.append(f"{titulo} ({gen}, {anio}, {rating})")
            
            # Mostrar resultados
            self.resultado_haskell.delete('1.0', tk.END)
            if resultados:
                resultado_texto = f"Películas filtradas por:\n"
                resultado_texto += f"- Género: {genero}\n"
                resultado_texto += f"- Año mínimo: {anio_min}\n"
                resultado_texto += f"- Rating mínimo: {rating_min}\n\n"
                resultado_texto += "RESULTADOS:\n" + "="*30 + "\n"
                resultado_texto += "\n".join(resultados)
            else:
                resultado_texto = "No se encontraron películas que cumplan los criterios."
            
            self.resultado_haskell.insert('1.0', resultado_texto)
            
        except ValueError as e:
            messagebox.showerror("Error", f"Error en los parámetros: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"Error ejecutando filtro Haskell: {e}")
    
    def recomendar_prolog(self):
        """Ejecuta recomendaciones usando Prolog"""
        if not self.prolog:
            messagebox.showerror("Error", "Prolog no está disponible")
            return
        
        try:
            tipo = self.tipo_recom_var.get()
            
            resultados = []
            
            if tipo == "recomendar_excelente":
                query = "recomendar_excelente(Pelicula)"
                for solucion in self.prolog.query(query):
                    resultados.append(solucion['Pelicula'])
            
            elif tipo == "recomendar_buena":
                query = "recomendar_buena(Pelicula)"
                for solucion in self.prolog.query(query):
                    resultados.append(solucion['Pelicula'])
            
            elif tipo == "recomendar_por_genero":
                genero = self.genero_prolog_var.get()
                query = f"recomendar_por_genero(Pelicula, {genero})"
                for solucion in self.prolog.query(query):
                    resultados.append(solucion['Pelicula'])
            
            elif tipo == "recomendar_genero_rating":
                genero = self.genero_prolog_var.get()
                rating_min = float(self.rating_prolog_var.get())
                query = f"recomendar_genero_rating(Pelicula, {genero}, {rating_min})"
                for solucion in self.prolog.query(query):
                    resultados.append(solucion['Pelicula'])
            
            # Mostrar resultados
            self.resultado_prolog.delete('1.0', tk.END)
            if resultados:
                resultado_texto = f"Recomendaciones usando: {tipo}\n"
                if tipo in ["recomendar_por_genero", "recomendar_genero_rating"]:
                    resultado_texto += f"Género: {self.genero_prolog_var.get()}\n"
                if tipo == "recomendar_genero_rating":
                    resultado_texto += f"Rating mínimo: {self.rating_prolog_var.get()}\n"
                resultado_texto += "\nRESULTADOS:\n" + "="*30 + "\n"
                resultado_texto += "\n".join([f"• {pelicula}" for pelicula in resultados])
            else:
                resultado_texto = "No se encontraron recomendaciones."
            
            self.resultado_prolog.insert('1.0', resultado_texto)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error ejecutando consulta Prolog: {e}")
    
    def run(self):
        """Ejecuta la aplicación"""
        self.root.mainloop()

def main():
    """Función principal"""
    try:
        app = SistemaRecomendacion()
        app.run()
    except ImportError:
        messagebox.showerror("Error", "PySwip no está instalado. Instale con: pip install pyswip")
    except Exception as e:
        messagebox.showerror("Error", f"Error iniciando la aplicación: {e}")

if __name__ == "__main__":
    main()