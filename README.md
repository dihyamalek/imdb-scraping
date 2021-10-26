# imdb-scraping

As part of my studies, I carried out this project for the Python module.

This project consists of retrieving data from the IMDB site. This is a list of 9000 movies ranked by popularity (5000 movie rating). The first step is to build a dataframe using scrapping and then analysis the data obtained.

## Getting started

- Install [MongoDB](https://www.mongodb.com/try/download/community)
- Create a db : `scraping-imdb-db`
- Start the server : `flask run`
- Ping the server `GET: http://localhost:5000//api/ping`
- API to start the scraping of the list of pages `POST: http://localhost:5000//api/scraping-movies-page-url`
- API to start the data scraping of each film `POST: http://localhost:5000//api/scraping-movies-data`
- API to start the scraping of each page of films retrieved in the list `POST: http://localhost:5000/api/movies`
- API to generate graphs from scraped data `POST: http://localhost:5000/api/generate-graphs`
- Graph page `GET: http://localhost:5000`

## Structure

- `app.py` : server main file
- `db/` : DB manipulation module
- `services/` : module of services used for scraping and generation of graphs
- `template/` : template html
- `static/` : generated assets (graph images)
- `db-data-scraped/` : export of the database with 9000 scraped films
