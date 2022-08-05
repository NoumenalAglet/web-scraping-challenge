# Dependencies
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Creating an instance of Flask app
app = Flask(__name__)

# Creating connection and database
app.config["MONGO_URI"]= "mongodb://localhost:27017/mars_data"
mongo = PyMongo(app)


# Setting up routes
@app.route("/")
def index():
    mars = mongo.db.mars.find_one()

    return render_template("index.html", mars=mars)

@app.route("/scrape")
def scrape():
    mars = mongo.db.mars
    mars_data = scrape_mars.scrape()
    mars.replace_one({}, mars_data, upsert=True)

    # Redirect back to home page
    return redirect("/", code = 302)

if __name__ == "__main__":
    app.run(debug=True)