# Sets up the routes for all the pages

from flask import Flask, render_template, request, make_response, redirect, url_for
from flask_caching import Cache
from config import TEMPLATES_PATH, TEXT_PATH
from application.helpers import *


import openai
import os


app = Flask(__name__, template_folder=TEMPLATES_PATH)
app.jinja_env.filters["is_active"] = is_active
app.jinja_env.filters["get_language_image"] = get_language_image

app.config["CACHE_TYPE"] = "simple"
app.config["CACHE_DEFAULT_TIMEOUT"] = 3600
cache = Cache(app)

openai.api_key = os.getenv('OPENAI_API_KEY')




@app.route("/")
def loading():
    """Renders the 'Loading' page of the website."""

    #response = make_response(render_template("loading.html"))
    #response.headers["Cache-Control"] = "public, max-age=3"

    #return response
    return render_template("home.html")


@app.route("/home")
@cache.cached()
def home():
    """Renders the 'Home' page of the website."""

    return render_template("home.html")


@app.route("/about")
@cache.cached()
def about():
    """Renders the 'About Me' page of the website."""

    content = read_description(f"{TEXT_PATH}/about.txt")

    return render_template("about.html", content=content)


@app.route("/skills")
@cache.cached()
def skills():
    """Renders the 'Skills' page of the website."""

    skills = get_skills(f"{TEXT_PATH}/skills.json")

    return render_template("skills.html", skills=skills)


@app.route("/portfolio")
@cache.cached()
def portfolio():
    """Renders the 'Portfolio' page of the website."""

    repos = get_repositories()

    return render_template("portfolio.html", repos=repos)


@app.route("/contact", methods=["GET", "POST"])
@cache.cached()
def contact():
    """Renders the 'Contact' page of the website."""

    # User reached route via POST
    if request.method == "POST":
        return render_template("result.html")

    # User reached route via GET
    return render_template("contact.html")



@app.route("/result")
@cache.cached()
def result():
    """Renders the 'Result' page of the website."""

    return render_template("result.html")

@app.route('/generate', methods=['POST'])
def generate():
    prompt = request.form['prompt']
    response = openai.ChatCompletion.create(
        messages=[
             {"role": "system", "content": "You are not only a knowledgeable history teacher but also novelist.you come from germany.you know most of thing about world war 2.Please convert the output results into Traditional Chinese."},
            {"role": "user", "content": prompt}
        ],
        model="gpt-3.5-turbo-0125",
        temperature = 0.5,
    )
    generated_text = response['choices'][0]['message']['content'].strip()
    return render_template('home.html', response=generated_text)
