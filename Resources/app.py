
import datetime as dt

import numpy as np
import pandas as pd
import sqlalchemy
from flask import Flask, jsonify
from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

engine = create_engine("sqlite:///Hawaii.sqlite",connect_args={'check_same_thread': False})
# reflect the database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

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
    """List all available api routes."""
    return (
        f"Available Routes for climate analysis!<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end"
    )
#########################################################################################

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return a list of rain fall for prior year"""
#  Convert the query results to a Dictionary using `date` as the key and `prcp` as the value.

#   * Return the JSON representation of your dictionary.

    last_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    rain = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date > last_year).\
        order_by(Measurement.date).all()
    rains = list(np.ravel(rain))
    return jsonify(rains)

#########################################################################################
@app.route("/api/v1.0/stations")
def stations():
    """Return a list of all station names"""
    # Query all stations
    data = session.query(Station.name).all()  
    station_names = list(np.ravel(data))
    return jsonify(station_names)
#########################################################################################
@app.route("/api/v1.0/tobs")
def tobs():
#      * query for the dates and temperature observations from a year from the last data point.
#   * Return a JSON list of Temperature Observations (tobs) for the previous year.

     last_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
     data1 = session.query(Measurement.date, Measurement.tobs).\
            filter(Measurement.date > last_year).\
             order_by(Measurement.date).all()
     all_tobs = list(np.ravel(data1))
     return jsonify(all_tobs)
#########################################################################################
@app.route("/api/v1.0/<start>")
def temperatures_start(start):
# """ Given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than 
#         and equal to the start date. 
#     """
#         #Parse the date 
    trip_arrive = dt.date(2017, 4, 1)

    data2 = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= trip_arrive).\
                    order_by(Measurement.date).all()
    # Convert list of tuples into normal list
    temperatures_start = list(np.ravel(data2))
    return jsonify(temperatures_start)

#########################################################################################
@app.route("/api/v1.0/<start>/<end>")
def temperatures_start_end(start, end):
    # """ When given the start and the end date, calculate the TMIN, TAVG, 
    #     and TMAX for dates between the start and end date inclusive.
    
    trip_arrive = dt.date(2017, 4, 1)
    trip_leave = dt.date(2017, 4, 15)
    data3 = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= trip_arrive).\
                filter(Measurement.date <= trip_leave).all()
    
    # Convert list of tuples into normal list
    temperatures_start_end = list(np.ravel(data3))
    return jsonify(temperatures_start_end)

#########################################################################################

if __name__ == "__main__":
    app.run(debug=True)
