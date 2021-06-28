import numpy as np
import pandas as pd
from plotnine import ggplot, aes, geom_bar, geom_line, theme, element_text, coord_flip, ylab, xlab, scale_x_datetime
from mizani.breaks import date_breaks
from mizani.formatters import date_format
import re

# Genere le graphe distribution des films par catégorie et le sauvegarde sous format png
def generate_graph_type_occurrences(movies):

    # Generer  une série pour l'apparition de chaque catégorie dans un film
    types = []
    for movie in movies:
        types += movie.types;

    # Generer un dataframe à partir de la série types et faire le counts des occurences de chaque type
    df = pd.DataFrame(types, columns=['type'])
    result = df["type"].value_counts().rename_axis('type').reset_index(name='occurrences')

    # Dessiner le graphe
    p = (
        ggplot(result, aes(x="reorder(type, -occurrences)", y="occurrences"))         
        + geom_bar(size=20, stat = "identity")
        + theme(axis_text_x = element_text(angle = 90, hjust = 1))
        + xlab("Category")
        + ylab("Occurrences")
    )
    p.save("static/generated_graph_type_occurrences.png", dpi = 600)

# Genere le graphe top 50 des budgets des films et le sauvegarde sous format png
def generate_graph_top50_budget(movies):
    # Filtrer la liste des films pour avoir uniquement ceux avec budget en dollar 
    # Dans le process de scrapping les films avec budget en dollar sont recuperés sans l'unité ($)
    movies = list(filter(lambda x: re.search("^[0-9]+$", x.budget), movies))

    # Convertir la colonne budget en int et la stocker dans une nouvelle colonne budget_int
    for movie in movies:
        movie.budget_int = int(movie.budget)
    
    # Trier les films par budget et prendre les 50 premiers
    movies = sorted(movies, key=lambda x: x.budget_int, reverse=True)[0:50]
    
    # Generer un dataframe avec les deux colonnes name et budget_int
    columns = ["name", "budget_int"]
    df = pd.DataFrame([[getattr(movie, columns) for columns in columns] for movie in movies], columns = columns)
    
    # Dessiner le graphe
    p = (
        ggplot(df, aes(x='reorder(name, budget_int)', y="budget_int"))         
        + geom_bar(size=20, stat = "identity", position="dodge")
        + theme(axis_text_y = element_text( size = 5))
        + coord_flip()
        + xlab("Title")
        + ylab("Budget")
    )
    p.save("static/generated_graph_top50_budget.png", dpi = 600)

# Genere le graphe top 20 films ayant générés le plus de revenu et le sauvegarder sous format png
def generate_graph_top20_cumulative_worldwide_gross(movies):
    # Filter la liste des films pour avoir uniquement ceux avec cumulative_worldwide_gross en dollar 
    # Dans le process de scrapping les films avec cumulative_worldwide_gross en dollar sont recuperés sans l'unité ($)
    movies = list(filter(lambda x: re.search("^[0-9]+$", x.cumulative_worldwide_gross), movies))
    
    # Convertir la colonne cumulative_worldwide_gross en int et la stocker dans une nouvelle colonne cumulative_worldwide_gross_int
    for movie in movies:
        movie.cumulative_worldwide_gross_int = int(movie.cumulative_worldwide_gross)
    
    # Trier les films par cumulative_worldwide_gross et prendre les 20 premiers
    movies = sorted(movies, key=lambda x: x.cumulative_worldwide_gross_int, reverse=True)[0:20]
    
    # Generer un data frame avec les deux colonnes name et cumulative_worldwide_gross_int
    columns = ["name", "cumulative_worldwide_gross_int"]
    df = pd.DataFrame([[getattr(movie, columns) for columns in columns] for movie in movies], columns = columns)
    
    # Dessiner le graphe
    p = (
        ggplot(df, aes(x='reorder(name, cumulative_worldwide_gross_int)', y="cumulative_worldwide_gross_int"))         
        + geom_bar(size=20, stat = "identity", position="dodge")
        + theme(axis_text_y = element_text( size = 5))
        + coord_flip()
        + xlab("Title")
        + ylab("Cumulative worldwide gross")
    )
    p.save("static/generated_graph_top20_cumulative_worldwide_gross.png", dpi = 600)

# Genere le graphe top 20 films ayant générés le moins de revenu et le sauvgarde sous format png
def generate_graph_less20_cumulative_worldwide_gross(movies):
    # Filter la liste des films pour avoir uniquement ceux avec cumulative_worldwide_gross en dollar 
    # Dans le process de scrapping les films avec cumulative_worldwide_gross en dollar sont recuperés sans l'unité ($)
    movies = list(filter(lambda x: re.search("^[0-9]+$", x.cumulative_worldwide_gross), movies))

    # Convertir la colonne cumulative_worldwide_gross en int et la stocker dans une nouvelle colonne cumulative_worldwide_gross_int
    for movie in movies: 
        movie.cumulative_worldwide_gross_int = int(movie.cumulative_worldwide_gross)

    # Trier les films par cumulative_worldwide_gross (ascendants) et prendre les 20 premiers
    movies = sorted(movies, key=lambda x: x.cumulative_worldwide_gross_int, reverse=False)[0:20]
    
    # Generer un dataframe avec les deux colonnes name et cumulative_worldwide_gross_int
    columns = ["name", "cumulative_worldwide_gross_int"]
    df = pd.DataFrame([[getattr(movie, columns) for columns in columns] for movie in movies], columns = columns)
    
    # Dessiner le graphe
    p = (
        ggplot(df, aes(x='reorder(name, -cumulative_worldwide_gross_int)', y="cumulative_worldwide_gross_int"))         
        + geom_bar(size=20, stat = "identity", position="dodge")
        + theme(axis_text_y = element_text( size = 5))
        + coord_flip()
        + xlab("Title")
        + ylab("Cumulative worldwide gross")
    )
    p.save("static/generated_graph_less20_cumulative_worldwide_gross.png", dpi = 600)

# Genere le graph top 10 des films par retour sur investissement et le sauvgarde sous format png
def generate_graph_top10_benefit(movies):
    # Filter la liste des films pour avoir uniquement ceux avec cumulative_worldwide_gross et budget en dollar 
    # Dans le process de scrapping les films avec cumulative_worldwide_gross (ou budget) en dollar sont recuperés sans l'unité ($)
    movies = list(filter(lambda x: re.search("^[0-9]+$", x.cumulative_worldwide_gross + x.budget), movies))
    
    # Calculer le bénifices generer par le film (cumulative_worldwide_gross - budget)
    for movie in movies: 
        movie.benefit = int(movie.cumulative_worldwide_gross) - int(movie.budget)
    
    # Trier les films par benefit et prendre les 10 premiers
    movies = sorted(movies, key=lambda x: x.benefit, reverse=True)[0:10]
    
    # Generer un data frame avec les deux colonnes name et benefit
    columns = ["name", "benefit"]
    df = pd.DataFrame([[getattr(movie, columns) for columns in columns] for movie in movies], columns = columns)
    
    # Dessiner le graphe
    p = (
        ggplot(df, aes(x='reorder(name, benefit)', y="benefit"))         
        + geom_bar(size=20, stat = "identity", position="dodge")
        + theme(axis_text_y = element_text( size = 5))
        + coord_flip()
        + xlab("Title")
        + ylab("Benifit")
    )
    p.save("static/generated_graph_top10_benefit.png", dpi = 600)

# Genere le graphe note moyenne par année de sortie de film et le sauvgarde sous format png
def generate_graph_average_rating_per_release_year(movies):
    # Filter et garder uniquement les film avec les deux données release_date et rating presentes
    movies = list(filter(lambda x: x.release_date != "XXX" and x.rating != "XXX", movies))
    
    # Convertir le rating en float (rating_float) et release_date en release_year (garder uniquement l'année)
    for movie in movies:
        movie.release_year = movie.release_date[-4:]
        movie.rating_float = float(movie.rating)
    
    # Créer le dataframe avec les deux colonne release_year et rating_float
    columns = ["release_year", "rating_float"]
    df = pd.DataFrame([[getattr(movie, columns) for columns in columns] for movie in movies], columns = columns)
    
    # convertir la colonne release_year et datetime
    df["release_year"] = pd.to_datetime(df['release_year'], format="%Y")
    
    # Generer un dataframe du groupby appliqué sur la colonne release_year et la moyenne appliquée sur la colonne rating_float
    df = df.groupby('release_year', sort=True).mean()["rating_float"].rename_axis('release_year').reset_index(name='rating_float')
    
    # Dessiner le graphe
    p = (
        ggplot(df, aes(x='release_year', y="rating_float"))         
        + geom_line()
        + scale_x_datetime(breaks=date_breaks('2 year'), labels=date_format('%Y'))
        + theme(axis_text_x = element_text(angle = 90, hjust = 1, size=5))
        + xlab("Year")
        + ylab("Rating average")
    )
    p.save("static/generated_graph_average_rating_per_release_year.png", dpi = 600)

# Genere le graphe distribution des revenus générés par genre de film et le sauvegarde sous format png
def generate_graph_cumulative_worldwide_gross_peer_type(movies):
    # Filter la liste des films pour avoir uniquement ceux avec cumulative_worldwide_gross en dollar 
    # Dans le process de scrapping les films avec cumulative_worldwide_gross en dollar sont recuperés sans l'unité ($)
    movies = list(filter(lambda x: re.search("^[0-9]+$", x.cumulative_worldwide_gross), movies))
    
    # Convertir la colonne cumulative_worldwide_gross en int et la stocker dans une nouvelle colonne cumulative_worldwide_gross_int
    for movie in movies: 
        movie.cumulative_worldwide_gross_int = int(movie.cumulative_worldwide_gross)
    
    # Generer les deux series des apparitions des types et de leurs cumulative_worldwide_gross (divisé par le nombre de type de chaque film)
    data = {"type":[], "cumulative_worldwide_gross":[]}
    for movie in movies:
        for type in movie.types:
            data["cumulative_worldwide_gross"].append(movie.cumulative_worldwide_gross_int / len(movie.types))
            data["type"].append(type)
    
    # Generer un dataframe avec les deux series type cumulative_worldwide_gross
    df = pd.DataFrame(data, columns = ["type", "cumulative_worldwide_gross"])

    # Generer un dataframe du groupby appliqué sur la colonne type et la somme appliquée sur la colonne cumulative_worldwide_gross
    df = df.groupby('type', sort=True).sum()["cumulative_worldwide_gross"].rename_axis('type').reset_index(name='cumulative_worldwide_gross')

    # Dessiner le graphe
    p = (
        ggplot(df, aes(x='reorder(type, cumulative_worldwide_gross)', y="cumulative_worldwide_gross"))         
        + geom_bar(size=20, stat = "identity")
        + coord_flip()
        + theme(axis_text_x = element_text(angle = 90, hjust = 1, size=5))
        + xlab("Category")
        + ylab("Cumulative worldwide gross")
    )
    p.save("static/generated_graph_cumulative_worldwide_gross_peer_type.png", dpi = 600)

# Genere le graphe nombre de films sortie par décennie et le sauvgarde sous format png
def generate_graph_number_of_films_released_per_decade(movies):
    # Generer une serie des décennies
    decades = []
    for movie in movies:
        if (movie.release_date != "XXX"): decades.append(movie.release_date[-4:-1] + "0")
    
    # Generer un dataframe à partir de la séries décennies et faire le counts des occurences de chaque décennies
    df = pd.DataFrame(decades, columns =['decades'])
    df = df["decades"].value_counts().rename_axis('decades').reset_index(name='occurrences')

    # Convertir decades en datetime
    df["decades"] = pd.to_datetime(df['decades'], format="%Y")

    # Dessiner le graphe
    p = (
        ggplot(df, aes(x='decades', y="occurrences"))         
        + geom_line()
        + scale_x_datetime(breaks=date_breaks('10 year'), labels=date_format('%Y'))
        + theme(axis_text_x = element_text(angle = 90, hjust = 1, size=5))
        + xlab("Decades")
        + ylab("Nb films released")
    )
    p.save("static/generated_graph_number_of_films_released_per_decade.png", dpi = 600)

    


    
    