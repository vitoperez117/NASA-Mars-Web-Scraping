from flask import Flask, jsonify, render_template, redirect
from flask_pymongo import PyMongo
from scrape_mars import scrape_all

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_scrape_db"
mongo = PyMongo(app)


@app.route('/')
def index ():
    entries = mongo.db.mars_news.find_one()
    return render_template('mars_scrape_index.html', entries=entries)
    

@app.route('/scrape')
def scrape():
    entries = mongo.db.mars_news
    entries_data = scrape_all()

    entries.update({}, entries_data, upsert=True)

    return redirect ("/", code=302)

if __name__ == '__main__':
    app.run(debug=True)