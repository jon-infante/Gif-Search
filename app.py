from flask import Flask, render_template, request
import requests
import json
from random import choice
import os
from dotenv import load_dotenv
load_dotenv()

TENOR_API_KEY = os.getenv("TENOR_API_KEY")
app = Flask(__name__)


@app.route('/')
def index():
    """Return homepage."""
    # Set parameters
    apikey = TENOR_API_KEY
    lmt = 12
    if request.args.get("search") != None:
        search_term = request.args.get("search")
    else:
        search_term = ""
    c_filter = "high"

    # Make dict from parameters
    params = {
        'q': search_term,
        'key': apikey,
        'limit': lmt,
        'content_filter': c_filter
        }

    # Call API and load results for search term
    r = requests.get("https://api.tenor.com/v1/search", params=params)
    if r.status_code == 200:  # If the request was successful
        first_gifs = json.loads(r.content)["results"]
    else:
        first_gifs = "None"

    # Render the 'index.html' template
    return render_template("index.html", first_gifs=first_gifs,
                           search=search_term)


@app.route('/trending')
def trending():
    """Return trending gifs"""
    apikey = TENOR_API_KEY
    lmt = 12
    c_filter = "high"

    # Make dict of parameters
    params = {
        'key': apikey,
        'limit': lmt,
        'contentfilter': c_filter
    }

    # Call API and load trending results
    r = requests.get("https://api.tenor.com/v1/trending", params=params)
    if r.status_code == 200:  # If the request was successful
        first_gifs = json.loads(r.content)["results"]
    else:
        first_gifs = None

    return render_template("index.html", first_gifs=first_gifs,
                           search="Trending")


@app.route('/random')
def random():
    """Return random gifs for a trending search term"""
    apikey = TENOR_API_KEY
    lmt = 12
    c_filter = "high"

    # Make dict of parameters
    params = {
        'key': apikey,
        'limit': lmt,
        'contentfilter': c_filter
    }

    # Call API and request a list of random search terms
    t = requests.get("https://api.tenor.com/v1/trending_terms", params=params)
    if t.status_code == 200:  # If the request was successful
        term_list = json.loads(t.content)["results"]
    else:
        term_list = None

    search = choice(term_list)

    # Make add random query term to params
    params['q'] = search

    # Call API and load random results
    r = requests.get("https://api.tenor.com/v1/random", params=params)
    if r.status_code == 200:  # If the request was successful
        first_gifs = json.loads(r.content)["results"]
    else:
        first_gifs = None

    return render_template("index.html", first_gifs=first_gifs,
                           search=search)


if __name__ == '__main__':
    app.run(debug=True)
