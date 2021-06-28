from flask import Flask, jsonify, request, Response, render_template
import time
from db import initialize_db, Movie
from services import scrape_movies_list, scrape_movie_data, generate_graph_type_occurrences, generate_graph_top50_budget, generate_graph_less20_cumulative_worldwide_gross, generate_graph_average_rating_per_release_year, generate_graph_top10_benefit, generate_graph_top20_cumulative_worldwide_gross, generate_graph_cumulative_worldwide_gross_peer_type, generate_graph_number_of_films_released_per_decade


# Instancier flask
app = Flask(__name__)

# Configurer la connection string pour se connecter à mongoDB
app.config['MONGODB_SETTINGS'] = {
    'host': 'mongodb://localhost:27017/scraping-imdb-db'
}

# Initialisation de la base de donnée
initialize_db(app)

# Route de test
@app.route("/api/ping", methods=['GET', 'POST'])
def ping():
    response = {
        'response': 'ping : OK !'
    }

    return jsonify(response)

# Route api pour lancer le scraping de la list des page
@app.route("/api/scraping-movies-page-url", methods=['POST'])
def scrapingMoviesPageUrl():
    ts = time.time()
    
    # Lancer le scraping de la liste des 9000 top rated long métrage
    scraped_movies_list = scrape_movies_list(9000)
    
    duration = time.time() - ts
    
    # Clean la collection movie
    Movie.objects.delete()
    
    # Inserer la liste des films scrapés dans la DB
    movie_instances = [Movie(**data) for data in scraped_movies_list]
    Movie.objects.insert(movie_instances, load_bulk=False)
    
    return {'scraping_duration': str(duration), "movies_number":str(len(scraped_movies_list))}, 200

# Route api pour lancer le scraping des pages de films
@app.route("/api/scraping-movies-data", methods=['POST'])
def scrapingMoviesData():
    # Recuperer la liste des films non scrappés (is_scraped=False) de la DB 
    movies = Movie.objects(is_scraped=False)
    scraped_data = []
    ts = time.time()
    
    for movie in movies:
        # Pour chaque film lancer le scrapping
        movie_data = scrape_movie_data(movie)
        
        # Marquer la film comme scrapé
        movie_data["is_scraped"] = True
        
        # update le film dans la db avec les donnée scrapés
        movie.update(**movie_data)
        scraped_data.append(movie_data)
    
    duration = time.time() - ts
    h = int(duration//3600)
    m = int((duration%3600)//60)
    s = int((duration%3600)%60)
    ms = int(((duration%3600)%60) * 1000)
    
    return {'scraping_duration': str(h) + ":" + str(m) + ":" + str(s) + ":" + str(ms), "scraped_movies": scraped_data}, 200

# Route api pour récuprer la liste des films dans la base de donnée
@app.route('/api/movies', methods=['GET'])
def get_movies():
    # Récuperer la liste des films de la db
    movies = Movie.objects().to_json()
    return Response(movies, mimetype="application/json", status=200)

# Route api pour génerer les graphs
@app.route('/api/generate-graphs', methods=['post'])
def generate_graphs():
    ts = time.time()
    
    # Récuperer la liste des films de la db
    movies = Movie.objects(is_scraped=True)
    
    # Lancer les differente fonction de generation des graphs
    generate_graph_type_occurrences(movies)
    generate_graph_top50_budget(movies)
    generate_graph_top20_cumulative_worldwide_gross(movies)
    generate_graph_less20_cumulative_worldwide_gross(movies)
    generate_graph_top10_benefit(movies)
    generate_graph_average_rating_per_release_year(movies)
    generate_graph_cumulative_worldwide_gross_peer_type(movies)
    generate_graph_number_of_films_released_per_decade(movies)
    
    duration = time.time() - ts
    h = int(duration//3600)
    m = int((duration%3600)//60)
    s = int((duration%3600)%60)
    ms = int(((duration%3600)%60) * 1000)
    
    return {'analyse_duration': str(h) + ":" + str(m) + ":" + str(s) + ":" + str(ms)}, 200

# Route de la page home qui affiche les graphs
@app.route('/', methods=['GET'])
def home():
    # Generer et renvoyer le template de la page home
    return render_template('home.html')