import pandas as pd
import numpy as np
import datetime as dt
import sqlalchemy
import black
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine, func
from sqlalchemy.orm import Session
from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
conn = engine.connect()

Base = automap_base()
Base.prepare(engine, reflect=True)

# Base.classes.keys()

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

app = Flask(__name__)


@app.route("/")
def welcome():
    return (
        f"Welcome to the Hawaii Climate Analysis API<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():

    prec = session.query(Measurement.date, Measurement.prcp).order_by(Measurement.date)

    prec_totals = []

    for data in prec:
        row = {}
        row["date"] = data.date
        row["prcp"] = data.date
        prec_totals.append(row)

    return jsonify(prec_totals)


@app.route("/api/v1.0/stations")
def stations():
    stations = session.query(Station.name)

    all_stations = []

    for data in stations:
        row = {}
        row["name"] = data.name
        all_stations.append(row)

    return jsonify(all_stations)


@app.route("/api/v1.0/tobs")
def temps():
    prior_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    temperature = session.query(Measurement.date, Measurement.tobs).filter(
        Measurement.date > prior_year
    )

    temps = []

    for data in temperature:
        row = {}
        row["date"] = data.date
        row["tobs"] = data.tobs
        temps.append(row)

    return jsonify(temps)


if __name__ == "__main__":
    app.run(debug=True)
