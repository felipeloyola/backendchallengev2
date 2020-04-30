from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import requests
from datetime import datetime
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////code/embeded.db'
db = SQLAlchemy(app)


class EarthQuake(db.Model):
    create_at = db.Column(db.DateTime, primary_key=True, default=datetime.utcnow)  #Llave primaria, fecha de insercion registro, valor por defecto
    campo = db.Column(db.String(200), nullable=True)  #descripción
    fecha_inicio = db.Column(db.DateTime, nullable=True)  #Fecha inicio búsqueda
    fecha_fin = db.Column(db.DateTime, nullable=True)  #Fecha fin búsqueda
    magnitud_min = db.Column(db.Float, nullable=True)  #Magnitud minima busqueda
    magnitud_max = db.Column(db.Float, nullable=True)  #Magnitud maxima busqueda
    salida = db.Column(db.Text, nullable=False, default="")  #Resultado busqueda (json)

db.create_all()

URL_BASE = "https://earthquake.usgs.gov/fdsnws/event/1/query"


@app.route('/searchEarthquake/getEarthquakesByDates/<starttime>/<endtime>/<minmagnitude>/', methods=['GET'])
def getEarthquakesByDates(starttime, endtime, minmagnitude):

    params={
            "format": "geojson",
            "starttime": starttime,
            "endtime": endtime,
            "minmagnitude": minmagnitude,
    }

    response = requests.get(makeURL(params))

    output = [ serialize(eq) for eq in response.json().get("features") ]

    eq = EarthQuake()
    eq.campo = "busqueda por fecha"
    eq.fecha_inicio = datetime.strptime(starttime, "%Y-%d-%m")
    eq.fecha_fin = datetime.strptime(endtime, "%Y-%d-%m")
    eq.magnitud_min = minmagnitude
    eq.magnitud_max = None
    eq.salida = json.dumps(output, indent=3)

    try:
        db.session.add(eq)
        db.session.commit()
    except Exception as e:
        raise e

    return jsonify(output)

@app.route('/searchEarthquake/getEarthquakesByMagnitudes/<minmagnitude>/<maxmagnitude>/', methods=['GET'])
def getEarthquakesByMagnitudes(minmagnitude, maxmagnitude):

    params={
            "format": "geojson",
            "minmagnitude": minmagnitude,
            "maxmagnitude": maxmagnitude
    }

    response = requests.get(makeURL(params))

    output = [serialize(eq) for eq in response.json().get("features")]

    eq = EarthQuake()
    eq.campo = "busqueda por magnitud"
    eq.fecha_inicio = None
    eq.fecha_fin = None
    eq.magnitud_min = minmagnitude
    eq.magnitud_max = maxmagnitude
    eq.salida = json.dumps(output, indent=3)

    try:
        db.session.add(eq)
        db.session.commit()
    except Exception as e:
        raise e

    return jsonify(output)

def serialize(eq):
    
    time = datetime.fromtimestamp(int(eq.get("properties").get("time") / 1000))
    updated = datetime.fromtimestamp(int(eq.get("properties").get("updated") / 1000))

    return {
        "mag": eq.get("properties").get("mag"),
        "place": eq.get("properties").get("place"),
        "time": time.strftime("%A, %B %-d, %Y %I:%M:%S.%f %p"),
        "updated": updated.strftime("%A, %B %-d, %Y %I:%M:%S.%f %p"),
        "alert": eq.get("properties").get("alert"),
        "status": eq.get("properties").get("status"),
        "tsunami": eq.get("properties").get("tsunami"),
        "magType": eq.get("properties").get("magType"),
        "type": eq.get("properties").get("type"),
        "title": eq.get("properties").get("title")
    }

def makeURL(params):

    url = f"{URL_BASE}?" + "&".join([ f"{key}={value}" for key, value in params.items() ])

    app.logger.debug(url)
    
    return url



