# backendchallengev2

# Install

```sh
$ docker build . -t backendchallengev2
```

# Test

```sh
$ docker run -it -p 5000:5000 backendchallengev2:latest pytest -v
```

# Run
```sh
$ docker run -it -p 5000:5000 backendchallengev2:latest flask run --host=0.0.0.0
$ curl 'http://localhost:5000/searchEarthquake/getEarthquakesByDates/2014-01-01/2015-01-02/5.5/'
$ curl 'http://localhost:5000/searchEarthquake/getEarthquakesByMagnitudes/5.5/6.0/'
```

