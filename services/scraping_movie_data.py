import requests
import time
import math
from bs4 import BeautifulSoup

MOVIE_PAGE_BASE_URL =  "https://www.imdb.com"

def scrape_movie_data(movie):
    ts = time.time()
    print(">> BEGIN Scraping : " + movie.name)
    
    result = {}
    # On recuprer la page du film
    movie_page = fetch_movie_page(movie.route_url)
    
    # On lance les differente functions qui recuprent les datas du film
    result["name"] = movie.name
    result["route_url"] = movie.route_url
    result["rating"] = get_rating(movie_page)
    result["score"] = get_score(movie_page)
    result["votes_nb"] = get_votes_nb(movie_page)
    result["director"] = get_director(movie_page)
    result["writers"] = get_writers(movie_page)
    result["movie_duration"] = get_movie_duration(movie_page)
    result["types"] = get_types(movie_page)
    result["release_date"] = get_release_date(movie_page)
    result["release_country"] = get_release_country(movie_page)
    result["filming_location"] = get_filming_location(movie_page)
    result["reviews_nb"] = get_reviews_nb(movie_page)
    result["storyline"] = get_storyline(movie_page)
    result["budget"] = get_budget(movie_page)
    result["opening_weekend_usa"] = get_opening_weekend_usa(movie_page)
    result["gross_usa"] = get_gross_usa(movie_page)
    result["cumulative_worldwide_gross"] = get_cumulative_worldwide_gross(movie_page)
    result["runtime"] = get_runtime(movie_page)
    result["color"] = get_color(movie_page)
    result["sound_mix"] = get_sound_mix(movie_page)
    result["aspect_ratio"] = get_aspect_ratio(movie_page)

    duration = time.time() - ts
    h = int(duration//3600)
    m = int((duration%3600)//60)
    s = int((duration%3600)%60)
    ms = int(((duration%3600)%60) * 1000)
    print("<< END Scraping : " + movie.name + " : " + str(h) + ":" + str(m) + ":" + str(s) + ":" + str(ms))

    return result

# Recupere la page du film
def fetch_movie_page(movie_route):
    print(">>>>>> BEGIN fetch_movie_page")
    response = requests.get(MOVIE_PAGE_BASE_URL + movie_route)
    print(">>>>>> END fetch_movie_page")
    return(BeautifulSoup(response.content,"html.parser"))

# Recupere le rating du film
def get_rating(movie_page):
    print(">>>>>> BEGIN get_rating")
    result = "XXX"
    elem = movie_page.find("span", {"itemprop": "ratingValue"})
    if (elem):
        result = elem.contents[0]
    print(">>>>>> END get_rating")
    return result

# Recupere le score
def get_score(movie_page):
    print(">>>>>> BEGIN get_score")
    metacritic_score_div = movie_page.find("div", {"class": "metacriticScore"})
    result = metacritic_score_div.find("span").contents[0] if metacritic_score_div else "XXX"
    print(">>>>>> END get_score")
    return result

# Recupere le nombre de vote
def get_votes_nb(movie_page):
    print(">>>>>> BEGIN get_votes_nb")
    result = "XXX"
    elem = movie_page.find("span", {"itemprop": "ratingCount"})
    if (elem):
        result = elem.contents[0].replace(",","")
    print(">>>>>> END get_votes_nb")
    return result

# Recupere le realisateur du film
def get_director(movie_page):
    print(">>>>>> BEGIN get_director")
    result = "XXX"
    elem = movie_page.find("h4", text="Director:")
    if (elem):
        result = elem.find_parent('div').find("a").contents[0]
    print(">>>>>> END get_director")
    return result

# Recupere la liste des scénaristes du film
def get_writers(movie_page):
    print(">>>>>> BEGIN get_writers")
    result = "XXX"
    elem = movie_page.find("h4", text="Writers:")
    if(elem):
        writers_a = elem.select('a[href*="/name/"]')
        result = list(map(lambda x : x.contents[0], writers_a))
    print(">>>>>> END get_writers")
    return result

# Recupere la durée du film
def get_movie_duration(movie_page):
    print(">>>>>> BEGIN get_movie_duration")
    result = "XXX"
    elem = movie_page.find("time")
    if (elem):
        result = elem.contents[0].strip().replace("\n", "").replace(" ", "")
    print(">>>>>> END get_movie_duration")
    return result

# Récupere la liste des category du film
def get_types(movie_page):
    print(">>>>>> BEGIN get_types")
    result = []
    elem = movie_page.find("h4", text="Genres:")
    if(elem):
        types_a = elem.find_parent('div').findAll("a")
        result = list(map(lambda x : x.contents[0].strip(), types_a))
    print(">>>>>> END get_types")
    return result

# Récupere la date de sortie du film
def get_release_date(movie_page):
    print(">>>>>> BEGIN get_release_date")
    result = "XXX"
    elem = movie_page.find("h4", text="Release Date:")
    if(elem):
        content = elem.find_parent('div').contents[2]
        result = content[0:content.index("(")].strip()
    print(">>>>>> END get_release_date")
    return result

# Récupere le pays de sortie du film
def get_release_country(movie_page):
    print(">>>>>> BEGIN get_release_country")
    result = "XXX"
    elem = movie_page.find("h4", text="Release Date:")
    if (elem):
        content = elem.find_parent('div').contents[2]
        result = content[content.index("(")+1:content.index(")")].strip()
    print(">>>>>> END get_release_country")
    return result

# Récupere le lieu de tournage du film
def get_filming_location(movie_page):
    print(">>>>>> BEGIN get_filming_location")
    result = []
    elem = movie_page.find("h4", text="Filming Locations:")
    if(elem):
        result = [elem.find_parent('div').find("a").contents[0]]
    print(">>>>>> END get_filming_location")
    return result

# Récupere le nb de commentaire du film
def get_reviews_nb(movie_page):
    print(">>>>>> BEGIN get_reviews_nb")
    result = "XXX"
    elem = movie_page.find("div", {"class": "titleReviewBarItem titleReviewbarItemBorder"})
    if (elem):
        text = elem.find("a").contents[0]
        result = text.replace(",","").replace("user", "").strip()
    print(">>>>>> END get_reviews_nb")
    return result

# Récupere le filmographie  du film
def get_storyline(movie_page):
    print(">>>>>> BEGIN get_storyline")
    result = "XXX"
    elem = movie_page.find("div", {"id": "titleStoryLine"})
    if (elem):
        result = elem.find("p").find("span").contents[0].strip()
    print(">>>>>> END get_storyline")
    return result

# Récupere le budget  du film
def get_budget(movie_page):
    print(">>>>>> BEGIN get_budget")
    result = "XXX"
    elem = movie_page.find("h4", text="Budget:")
    if (elem):
        text = elem.find_parent('div').contents[2]
        result = text.replace("$","").replace("\n", "").replace(",", "").strip()
    print(">>>>>> END get_budget")
    return result

# Récupere le opening weekend usa du film
def get_opening_weekend_usa(movie_page):
    print(">>>>>> BEGIN get_opening_weekend_usa")
    result = "XXX"
    elem = movie_page.find("h4", text="Opening Weekend USA:")
    if(elem):
        text = elem.find_parent('div').contents[2]
        result = text.replace("$","").replace("\n", "").replace(",", "").strip()
    print(">>>>>> END get_opening_weekend_usa")
    return result

# Récupere le gross usa du film
def get_gross_usa(movie_page):
    print(">>>>>> BEGIN get_gross_usa")
    result = "XXX"
    elem = movie_page.find("h4", text="Gross USA:")
    if (elem):
        text = elem.find_parent('div').contents[2]
        result = text.replace("$","").replace("\n", "").replace(",", "").strip()
    print(">>>>>> END get_gross_usa")
    return result

# Récupere le cumulative worldwide gross du film
def get_cumulative_worldwide_gross(movie_page):
    print(">>>>>> BEGIN get_cumulative_worldwide_gross")
    result = "XXX"
    elem = movie_page.find("h4", text="Cumulative Worldwide Gross:")
    if (elem):
        text = elem.find_parent('div').contents[2]
        result = text.replace("$","").replace("\n", "").replace(",", "").strip()
    print(">>>>>> END get_cumulative_worldwide_gross")
    return result

# Récupere le runtime du film
def get_runtime(movie_page):
    print(">>>>>> BEGIN get_runtime")
    result = "XXX"
    elem = movie_page.find("h4", text="Runtime:")
    if (elem):
        result = elem.find_parent('div').find("time").contents[0].replace(" ","")
    print(">>>>>> END get_runtime")
    return result

# Récupere le color du film
def get_color(movie_page):
    print(">>>>>> BEGIN get_color")
    result = []
    elem = movie_page.find("h4", text="Color:")
    if (elem):
        colors_a = elem.find_parent('div').findAll("a")
        result = list(map(lambda x : x.contents[0].strip(), colors_a))
    print(">>>>>> END get_color")
    return result

# Récupere le sound mix du film
def get_sound_mix(movie_page):
    print(">>>>>> BEGIN get_sound_mix")
    result = []
    elem = movie_page.find("h4", text="Sound Mix:")
    if (elem):
        sound_mix_a = elem.find_parent('div').findAll("a")
        result = list(map(lambda x : x.contents[0].strip(), sound_mix_a))
    print(">>>>>> END get_sound_mix")
    return result

# Récupere le ratio d'affichage du film
def get_aspect_ratio(movie_page):
    print(">>>>>> BEGIN get_aspect_ratio")
    result = "XXX"
    elem = movie_page.find("h4", text="Aspect Ratio:")
    if (elem):
        text = elem.find_parent('div').contents[2]
        result = text.replace("\n", "").strip()
    print(">>>>>> END get_aspect_ratio")
    return result

__all__ = ["scrape_movie_data"]