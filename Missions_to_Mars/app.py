#Import Dependencies
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars


#Create an instance of the Flask app
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

#mongo.db.mars_data.insert_many(mars_data)







#Create in dex route that makes the html template
@app.route("/")
def home():
    
    #locate the Mars data
    mars_data = mongo.db.mars_data.find_one()
    
    #Return Template and data
    return render_template("index.html", mars_data=mars_data)

# Route that will trigger scrape function
@app.route("/scrape")
def scrape(): 

    # Run scrapped functions
    
    mars_facts = scrape_mars.scrape()
    mongo.db.mars.drop()
    mongo.db.mars.insert_one(mars_facts)
    
    
    return redirect("/", code=302)

if __name__ == "__main__": 
    app.run(debug= True)

