# Import Flask
from flask import Flask, jsonify

# Import Dependancies
from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime as dt

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, func

# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

# Create an app, being sure to pass __name__
app = Flask(__name__)

# 1. Define what to do when a user hits the index route
@app.route("/")
def home():
    return(
        f"Welcome to My API!<br/>"
        f"Available Routes:<br/>"
        f"Precipitation: /api/v1.0/precipitation<br/>"
        f"List of Stations: /api/v1.0/stations<br/>"
        f"Temperature for one year: /api/v1.0/tobs<br/>"
        f"Temperature statistics from the start date: /api/v1.0/start<br/>"
        f"Temperature statistics from start to end dates: /api/v1.0/start/end"
    )

# 2. Define what to do when a user hits the /api/v1.0/precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    recent_date = session.query(measurement.date).order_by(measurement.date.desc()).first()[0]
    conv_recent_date = dt.datetime.strptime(recent_date, '%Y-%m-%d').date()
    one_year = conv_recent_date - dt.timedelta(days=365)
    sel = [measurement.date, measurement.prcp]
    query_result = session.query(*sel).filter(measurement.date <= conv_recent_date).filter(measurement.date > one_year).all()    
    session.close()

    precipitation = []
    for date, prcp in query_result:
            prcp_dict = {}
            prcp_dict["Date"] = date
            prcp_dict["Precipitation"] = prcp
            precipitation.append(prcp_dict)
    return jsonify(precipitation)

# 3. Define what to do when a user hits the /api/v1.0/stations route
@app.route("/api/v1.0/stations")
def stations():
    station = Base.classes.station
    # Create our session (link) from Python to the DB
    session = Session(engine)
    station_list_query = session.query(station.station, station.name).all()
    session.close()

    stations_list = []
    for station, name in station_list_query:
         stations_dict = {}
         stations_dict['station'] = station
         stations_dict['name'] = name
         stations_list.append(stations_dict)
    return jsonify(stations_list)

# 4. Define what to do when a user hits the /api/v1.0/tobs route
@app.route("/api/v1.0/tobs")
def tobs():
    print("Server received request for 'Temperature Observations' page...")
    return "Welcome to my 'Temperature Observations' page!"

# 5. Define what to do when a user hits the /api/v1.0/<start> route
@app.route("/api/v1.0/<start>")
def start():
    print("Server received request for 'About' page...")
    return "Welcome to my 'About' page!"

# 6. Define what to do when a user hits the /api/v1.0/<start>/<end> route
@app.route("/api/v1.0/<start>/<end>")
def end():
    print("Server received request for 'About' page...")
    return "Welcome to my 'About' page!"

if __name__ == "__main__":
    app.run(debug=True)
