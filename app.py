# Third Party
import pymongo
from flask_pymongo import PyMongo
from flask import Flask, render_template, redirect, flash

# Custom
from scripts.scrape_for_mars_data import (
    scrape_mars_NASA_articles
    , scrape_mars_NASA_featured_image
    , scrape_mars_weather_tweets
    , scrape_mars_space_facts_html_table
    , scrape_mars_hemisphere_image_urls
)
from config import db_password, secret_key

app = Flask(__name__)
app.config['DEBUG'] = True
app.config["MONGO_URI"] = f"mongodb+srv://{db_password}@cluster0.mvmcg.mongodb.net/MissionToMars?retryWrites=true&w=majority"
app.secret_key = secret_key
mongo = PyMongo(app)

@app.route("/")
def index():
    MarsData = mongo.db.MarsData.find_one()
    return render_template("index.html", MarsData=MarsData)


@app.route("/scrape")
def scrape():
    MarsDataCollection = mongo.db.MarsData

    try:
        mars_NASA_articles = scrape_mars_NASA_articles()
        newest_mars_NASA_article_title = mars_NASA_articles[0]["title"]
        newest_mars_NASA_article_teaser = mars_NASA_articles[0]["teaser"]
        print(f"{newest_mars_NASA_article_title}:\n{newest_mars_NASA_article_teaser}")

        mars_featured_image = scrape_mars_NASA_featured_image()
        print(mars_featured_image)

        mars_weather = scrape_mars_weather_tweets()[0]
        print(mars_weather)

        mars_space_facts_html_table = scrape_mars_space_facts_html_table()
        print(mars_space_facts_html_table)

        mars_hemisphere_image_urls = scrape_mars_hemisphere_image_urls()
        print(mars_hemisphere_image_urls)

        MarsData = {
            "news_title": newest_mars_NASA_article_title
            , "news_teaser": newest_mars_NASA_article_teaser
            , "featured_image_url" : mars_featured_image
            , "weather": mars_weather
            , "facts": mars_space_facts_html_table
            , "hemisphere_image_urls": mars_hemisphere_image_urls
        }

        MarsDataCollection.update({}, MarsData, upsert=True)
        flash("Bot successfully retrieved new Mars data.", "success")
    except Exception as e:
        print(e)
        flash("Bot failed to retrieve new Mars data. Defaulting to data from last successful scrape.", "danger")
    
    return redirect("/")


if __name__ == '__main__':
    app.run()