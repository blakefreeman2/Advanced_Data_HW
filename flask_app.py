
# ## Step 2 - Climate App

# Now that you have completed your initial analysis, design a Flask API based on the queries that you have just developed.

# * Use FLASK to create your routes.

#Import of Dependencys
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

import datetime as dt
from datetime import date
from dateutil.relativedelta import relativedelta

# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

# Flask Setup
app = Flask(__name__)

# Flask Routes

#   * Home page.

#   * List all routes that are available.

@app.route("/")
def route_avalible():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"<br/>"
        f"/api/v1.0/stations<br/>"
        f"<br/>"
        f"/api/v1.0/tobs<br/>"
        f"<br/>"
        f"/api/v1.0/start<br/>"
        f"Follow this format: /api/v1.0/yyyy-mm-dd<br/>"
        f"<br/>"
        f"/api/v1.0/start/end<br/>"
        f"Follow this format: /api/v1.0/yyyy-mm-dd/yyy-mm-dd<br/>"
    )
# `/api/v1.0/precipitation`

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return a Json of Precipitation Dates and actual precipitation"""
    # Convert the query results to a Dictionary using `date` as the key and `prcp` as the value.
    results = session.query(Measurement.date, Measurement.prcp).all()

    # Return the JSON representation of your dictionary.
    all_precipitation = []
    for date, prcp in results:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["prcp"] = prcp
        all_precipitation.append(precipitation_dict)

    return jsonify(all_precipitation)


@app.route("/api/v1.0/stations")
def stations():
    """Return a list of JSON list of stations from the dataset."""
    # Return a JSON list of stations from the dataset.
    results = session.query(Station.name, Station.station).all()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

# `/api/v1.0/tobs`

@app.route("/api/v1.0/tobs")
def tobs():
    """Return a list of JSON list of stations from the dataset."""
    # Query for the dates and temperature observations from a year from the last data point.

    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first().date

    current_date = dt.datetime.strptime(last_date,'%Y-%m-%d').date()
    prior_year = dt.datetime.strptime(last_date, '%Y-%m-%d').date() + relativedelta(years=-1)

    results = session.query(session.query(Measurement.date, Measurement.prcp)).filter(Measurement.date >= prior_year).all()

    # Convert list of tuples into normal list
    all_tobs = list(np.ravel(results))
    #  Return a JSON list of Temperature Observations (tobs) for the previous year.
    return jsonify(all_tobs)


# * `/api/v1.0/<start>` 

@app.route("/api/v1.0/<start>")
def calc_temps(start):
    """TMIN, TAVG, and TMAX for a list of dates.
    
    Args:
        start (string): A date string in the format %Y-%m-%d
        end_date (string): A date string in the format %Y-%m-%d
        
    Returns:
        TMIN, TAVE, and TMAX
    """
    
    return_start = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).group_by(Measurement.date).all()


    # Convert list of tuples into normal list
    all_tobs = []
    for date, TMIN, TAVG, TMAX in return_start:
        toods_dict = {}
        toods_dict["date"] = date
        toods_dict["TMIN"] = TMIN
        toods_dict["TAVG"] = TAVG
        toods_dict["TMAX"] = TMAX
        all_tobs.append(toods_dict)
        
    #  Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
    return jsonify(all_tobs)


##   * Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.

#   * When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.

#   * When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.

@app.route("/api/v1.0/<start>/<end>")
def calc_temps_dates(start, end):
    """TMIN, TAVG, and TMAX for a list of dates.
    
    Args:
        start (string): A date string in the format %Y-%m-%d
        end_date (string): A date string in the format %Y-%m-%d
        
    Returns:
        TMIN, TAVE, and TMAX
    """
    
    return_start_end = session.query(Measurement.date,func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).group_by(Measurement.date).all()


    # Convert list of tuples into normal list
    all_tobs_start_end = []
    for date, TMIN, TAVG, TMAX in return_start_end:
        toods_dict = {}
        toods_dict["date"] = date
        toods_dict["TMIN"] = TMIN
        toods_dict["TAVG"] = TAVG
        toods_dict["TMAX"] = TMAX
        all_tobs_start_end.append(toods_dict)
        
    #  Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
    return jsonify(all_tobs_start_end)


# `/api/v1.0/<start>/<end>`

#   * Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.

#   * When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.

#   * When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.

if __name__ == '__main__':
    app.run(debug=True)
