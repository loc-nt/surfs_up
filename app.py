
import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# access to SQLite database:
engine = create_engine("sqlite:///hawaii.sqlite")

# map the database first:
Base = automap_base()

# reflect the database into our classes:
Base.prepare(engine, reflect=True)

# create var for each of the classes:
Measurement = Base.classes.measurement
Station = Base.classes.station

# create session link:
session = Session(engine)

# setup Flask app Instance (a singular version of something):
app = Flask(__name__)

# Define the starting point , aka the root
@app.route('/') # The forward slash is commonly known as the highest level of hierarchy in any computer system.

# welcome function:
def welcome():
	return(
    '''
    Welcome to the Climate Analysis API!
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end
    ''')

# create a new route for precipitation:
@app.route("/api/v1.0/precipitation")
# create precipitation function:
def precipitation():
	# 1 year ago:
	prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
	# get the date and precipitation for the previous year
	precipitation = session.query(Measurement.date, Measurement.prcp).\
      filter(Measurement.date >= prev_year).all()
	# get the results, and return nito Json file:
	precip = {date: prcp for date, prcp in precipitation}
	return jsonify(precip)

# crea a new route for stations:
@app.route("/api/v1.0/stations")
# create station function:
def stations():
	# get all the stations:
	results = session.query(Station.station).all()
	# unravel the result, and convert into a list, then return json file:
	stations = list(np.ravel(results))
	return jsonify(stations)

# create a new route for tobs:
@app.route("/api/v1.0/tobs")	
def temp_monthly():
	# 1 year ago:
	prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
	# query the temp from the primary (most active) station, within last 1 year:
	results = session.query(Measurement.tobs).\
		filter(Measurement.station == 'USC00519281').\
		filter(Measurement.date >= prev_year).all()
	# unravel the result, and convert into a list, then return json file:
	temps = list(np.ravel(results))
	return jsonify(temps)
	
# new routes, with parameters:
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")

def stats(start=None, end=None):
	sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
	# if no end_date input
	if not end:
		# the asterisk is used to indicate there will be multiple results for our query: minimum, average, and maximum temperatures.
		results = session.query(*sel).filter(Measurement.date <= start).all()
		temps = list(np.ravel(results))
		return jsonify(temps)
	
	results = session.query(*sel).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
	temps = list(np.ravel(results))
	return jsonify(temps)