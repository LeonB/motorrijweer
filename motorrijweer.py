# TODOS
# - remove pytz (600 files!! and I only need one)

import flask
import flaskext
from flaskext.cache import Cache
from flaskext.babel import Babel

# First set up app + cache (it may be used by other modules)
app = flask.Flask(__name__)
app.config.from_pyfile('motorrijweer.nl.cfg')
app.debug = True
app.cache = Cache(app)
app.babel = Babel(app)

import mytime
import weather
import models
import controllers
import decorators
import jinja_filters
import jinja_tests

@app.before_request
def before_request():
    app.timezone = flaskext.babel.get_timezone()
    app.jinja_env.globals['now'] = mytime.datetime.now()

@app.errorhandler(404)
def page_not_found(e):
    return flask.render_template('404.jinja'), 404

@app.route('/')
def index():
    provincies = weather.Provincie.all()
    return flask.render_template('index.jinja', provincies=provincies)

## REGIO ##
@app.route('/regio/<regio>')
def regio_redirect(regio):
    if (mytime.datetime.today().hour < 20):
        return flask.redirect('/regio/%(regio)s/vandaag' % {'regio': regio}, 302)
    else:
        return flask.redirect('/regio/%(regio)s/morgen' % {'regio': regio}, 302)

@app.cache.memoize(timeout=60*5) # 5 minutes
@app.route('/regio/<regio>/<datum_str>')
def regio(regio, datum_str = 'vandaag'):
    # Does the regio exist?
    regio = weather.Regio.by_id(regio.lower())
    if not regio:
        return flask.abort(404)

    # Change input to real date object
    datum = _datums(datum_str)

    weer = weather.Weather().from_gae(regio=regio, datum=datum)
    return flask.render_template('regio.jinja', weer=weer, regio=regio, datum=datum)

## PROVINCIE ##
@app.route('/provincie/<provincie>')
def provincie_redirect(provincie):
    if (mytime.datetime.today().hour < 20):
        return flask.redirect('/provincie/%(provincie)s/vandaag' % {'provincie': provincie}, 302)
    else:
        return flask.redirect('/provincie/%(provincie)s/morgen' % {'provincie': provincie}, 302)

@app.cache.memoize(timeout=60*5) # 5 minutes
@app.route('/provincie/<provincie>/<datum_str>')
def provincie(provincie, datum_str = 'vandaag'):
    # Does the provincie exist?
    provincie = weather.Provincie.by_id(provincie.lower())
    if not provincie:
        return flask.abort(404)

    # Change input to real date object
    datum = _datums(datum_str)

    weer = weather.Weather().from_gae(provincie=provincie, datum=datum)
    return flask.render_template('provincie.jinja', weer=weer, provincie=provincie, datum=datum)

def _datums(datum_str):
    # Change input to real date object
    if datum_str == 'vandaag':
        datum = mytime.date.today()
    elif datum_str == 'morgen':
        datum = mytime.date.tomorrow()
    elif datum_str == 'overmorgen':
        datum = mytime.date.day_after_tomorrow()
    elif datum_str == 'gisteren':
        datum = mytime.date.yesterday()
    elif datum_str == 'eergisteren':
        datum = mytime.date.day_before_yesterday()
    else:
        datum = mytime.datetime.strptime(datum_str, '%d%m%Y').date()

    return datum

def _link_back(datum):
    datum = datum - mytime.timedelta(days=1)
    datum_str = jinja_filters.datestr(datum)
    return (datum_str if datum_str else datum)

def _link_forward(datum):
    datum = datum + mytime.timedelta(days=1)
    datum_str = jinja_filters.datestr(datum)
    return (datum_str if datum_str else datum)

@app.route('/tasks/wunderground/forecasts/hourly')
def tasks_wunderground_forecasts_hourly():
    return str(controllers.tasks.wunderground.forecasts.hourly())

@app.route('/tasks/wunderground/forecasts/daily')
def tasks_wunderground_forecasts_daily():
    return str(controllers.tasks.wunderground.forecasts.daily())

@app.route('/tasks/regeneratecijfers')
def tasks_regeneratecijfers():
    for dbForecast in models.Forecast.all():
        forecast = weather.Forecast.from_gae(dbForecast)
        dbForecast.cijfer = forecast.generate_cijfer()
        dbForecast.put()

    return 'OK'

@app.route('/test_cijfers')
def test_cijfers():
    obj = weather.Forecast()
    obj.temperatuur = 0
    obj.neerslagkans = 1.0
    obj.windkracht = 1 #in km/h
    obj.neerslag_in_mm = 0.0
    #return str(obj.cijfer_windkracht(weather.Beaufort.from_kmh(obj.windkracht)))
    obj.cijfer = obj.generate_cijfer()

    #return str(obj.cijfer)

    gegevens = {}
    for temp in range(-6, 36, 3):
        for neerslag_in_mm in range(0, 11, 1):
            neerslag_in_mm = neerslag_in_mm/4.0
            for windkracht in (0, 3, 8.5, 15.5, 24, 33.5, 44, 55.5, 68, 81.5,
                               95.5, 110, 120):
                #windkracht = weather.Beaufort.from_kmh(windkracht)
                if not gegevens.has_key(temp):
                    gegevens[temp] = {}
                if not gegevens[temp].has_key(neerslag_in_mm):
                    gegevens[temp][neerslag_in_mm] = {}
                if not gegevens[temp][neerslag_in_mm].has_key(windkracht):
                    gegevens[temp][neerslag_in_mm][windkracht] = []

                obj = weather.Forecast()
                obj.temperatuur = temp
                obj.neerslagkans = 1.0
                obj.windkracht = windkracht
                obj.neerslag_in_mm = neerslag_in_mm
                obj.cijfer = obj.generate_cijfer()
                gegevens[temp][neerslag_in_mm][windkracht].append(obj)

    return flask.render_template('test_cijfers.jinja', gegevens=gegevens)

# @app.route('/tasks/update_datastore')
# def update_datastore():
#     for forecast in models.Forecast.gql('ORDER BY datapunt_van DESC'):
#         forecast.put()

@app.route('/stations')
def stations():
    return str(weather.Region.by_id('zeeland'))
