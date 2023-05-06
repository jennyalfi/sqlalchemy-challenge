# Import the dependencies.
from flask import Flask, jsonify

import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt



# List all the available routes.
#Define what to do when a user hits the route
# @app.route("/")
# def home():
#     print("Server received request for 'Home' page...")
#     return "Welcome to my 'Home' page!"

# @app.route("/about")
# def about():
#     name = "Jen"
#     location = "California"

#     return f"My name is {name}, and I live in {location}."

# @app.route("/contact")
# def contact():
#     email = "jen@fakeemail.com"

#     return f"Questions? Comments? Please send an email to {email}."




# 2.) API precipitation
# Convert the query results from your precipitation analysis 
# (i.e. retrieve only the last 12 months of data) to a dictionary 
# using date as the key and prcp as the value.


# Return the JSON representation of your dictionary.

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
base = automap_base()

# reflect the tables
base.prepare(autoload_with=engine)

# Save references to each table
measurement = base.classes.measurement

station = base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """These are the available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/station<br/>"
        f"/api/v1.0/date<br/>"
        f"/api/v1.0/prcp<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/yyyy-mm-dd<br/>"
        f"/api/v1.0/temp/start/end<br/>"
        f"/api/v1.0/longitude<br/>"
        f"/api/v1.0/elevation<br/>"
    )


# 2.) API precipitation
# Convert the query results from your precipitation analysis 
# (i.e. retrieve only the last 12 months of data) to a dictionary 
# using date as the key and prcp as the value.

# Return the JSON representation of your dictionary.


@app.route("/api/v1.0/precipitation")
def precipitation():

    """Return a list of precipitation data including the name, age, and sex of each passenger"""
    # Query all precipitation
    last_year = dt.date(2017,8,23)-dt.timedelta(days=365)

    results = session.query(measurement.date, measurement.prcp).filter(measurement.date >= last_year).all()


    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    all_precipitation = []
    for date, prcp in results:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["precipitation"] = prcp
        all_precipitation.append(precipitation_dict)

    return jsonify(all_precipitation)




# 3.) API stations
# Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def stations():

    """Return a list of precipitation data including the name, age, and sex of each passenger"""
    # Query all precipitation

    results = session.query(station.station).all()


    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    # all_precipitation = []
    # for date, prcp in results:
    #     precipitation_dict = {}
    #     precipitation_dict["date"] = date
    #     precipitation_dict["precipitation"] = prcp
    #     all_precipitation.append(precipitation_dict)
    stations = list(np.ravel(results))

    return jsonify(stations)


# 4.) API tobs (like one did but add filte for station)
# Query the dates and temperature observations of the 
# #most-active station for the previous year of data.

# Return a JSON list of temperature observations for the previous year.




# 5.) API start and end
# Return a JSON list of the minimum temperature, the average temperature, 
# and the maximum temperature for a specified start or start-end range.

# For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date.

#For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive.
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")

def temp(start=None,end=None):

    """Return a list of temperature data including the name, age, and sex of each passenger"""
    sel = [func.min(measurement.tobs),func.max(measurement.tobs),func.avg(measurement.tobs)]
    if not end:
        results = session.query(*sel).filter(measurement.date >= start).all()
        session.close()
        temps = list(np.ravel(results))
        return jsonify (temps)
   
    results = session.query(*sel).filter(measurement.date >= start).filter(measurement.date <= end).all()
    session.close()
    temps = list(np.ravel(results))
    return jsonify (temps)
   




# Define main behavior
if __name__ == "__main__":
    app.run(debug=True)