# Third Party
import pymongo
from flask_pymongo import PyMongo
from flask import Flask, render_template, redirect

# Custom
from scripts.scrape_mars import scrape
from config import db_password

app = Flask(__name__)
app.config['DEBUG'] = True
app.config["MONGO_URI"] = f"mongodb+srv://{db_password}@cluster0.mvmcg.mongodb.net/MissionToMars?retryWrites=true&w=majority"
mongo = PyMongo(app)

@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)

@app.route("/scrape")
def scrape_web():
    mars = mongo.db.mars
    mars_data = scrape()
    mars.update({}, mars_data, upsert=True)
    return redirect("/")

if __name__ == '__main__':
    app.run()