import os
import tempfile

import pytest

import app


@pytest.fixture
def client():
    db_fd, tmp_path = tempfile.mkstemp()
    app.app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:////{tmp_path}"
    app.app.config['TESTING'] = True

    with app.app.test_client() as client:
        with app.app.app_context():
            app.db.create_all()
        yield client

    os.close(db_fd)
    os.unlink(tmp_path)

def test_getEarthquakesByMagnitudes(client):

    magnitud_min = 5.5
    magnitud_max = 6.5

    rv = client.get(f'/searchEarthquake/getEarthquakesByMagnitudes/{magnitud_min}/{magnitud_max}/')
    assert len(app.EarthQuake.query.all()) == 1

    search = app.EarthQuake.query.order_by(app.EarthQuake.create_at).first()

    assert search.campo == "busqueda por magnitud"
    assert search.magnitud_min == magnitud_min
    assert search.magnitud_max == magnitud_max
    assert search.fecha_inicio is None 
    assert search.fecha_fin is None 

def test_getEarthquakesByDates(client):

    fecha_inicio = "2014-01-01"
    fecha_fin = "2015-01-02"
    magnitud_min = 5.5

    rv = client.get(f'/searchEarthquake/getEarthquakesByDates/{fecha_inicio}/{fecha_fin}/{magnitud_min}/')

    assert len([eq for eq in rv.get_json() if eq.get("mag") < magnitud_min]) == 0

    assert len(app.EarthQuake.query.all()) == 1

    search = app.EarthQuake.query.order_by(app.EarthQuake.create_at).first()

    assert search.campo == "busqueda por fecha"
    assert search.magnitud_min == magnitud_min
    assert search.magnitud_max is None
    assert search.fecha_inicio.strftime("%Y-%d-%m") == fecha_inicio
    assert search.fecha_fin.strftime("%Y-%d-%m") == fecha_fin
