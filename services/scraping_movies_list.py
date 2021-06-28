import requests
import math
from bs4 import BeautifulSoup

MOVIE_LIST_PAGE_URL =  "https://www.imdb.com/search/title/?title_type=feature&num_votes=5000,&view=simple&sort=user_rating,desc&count=250"

# Retourne la liste des films contenus dans une page
def get_movies_list(movies_page):
    result = []
    movie_containers = movies_page.findAll("span", {"class": "lister-item-header"})
    for movie_index in range(0, len(movie_containers)):
        movie_a = movie_containers[movie_index].find("a")
        movie_name = movie_a.contents[0]
        movie_route = movie_a.attrs["href"]
        result.append({"name": movie_name, "route_url": movie_route})
    return result

# Recupere la page de la liste des films à la position page_number
def get_movies_list_page(page_number):
    
    # On récupère la page
    response = requests.get(MOVIE_LIST_PAGE_URL + "&start=" + str((page_number - 1) * 250 + 1))
    
    # On parse et retourne la structure html de la page
    return(BeautifulSoup(response.content,"html.parser"))

# scrapper movies_nb premiers top rated long métrage
def scrape_movies_list(movies_nb):
    # calculer le nbr de page à scrapper (250 films par page)
    page_nb = math.ceil(movies_nb / 250)
    result = []

    # Boucler sur le nombre de pages calculées et lancer le scraping de chaque page
    for page_index in range(1, page_nb + 1):
        # Recuperer la page de la liste des films
        movies_page =  get_movies_list_page(page_index)
        
        # Scraper la page de la liste des films
        result += get_movies_list(movies_page)
    return result

__all__ = ["scrape_movies_list"]

