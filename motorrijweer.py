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
    return flask.render_template('404.tpl'), 404

@app.route('/locatie/<locatie>')
def locatie_redirect(locatie):
    if (mytime.datetime.today().hour < 20):
        return flask.redirect('/locatie/%(locatie)s/vandaag' % {'locatie': locatie}, 302)
    else:
        return flask.redirect('/locatie/%(locatie)s/morgen' % {'locatie': locatie}, 302)

@app.cache.memoize(timeout=60*5)
@app.route('/locatie/<locatie>/<datum_str>')
def locatie(locatie, datum_str = 'vandaag'):
    # Does the location exist?
    if locatie.upper() not in weather.Station.all_ids():
        return flask.abort(404)

    # Change input to real date object
    datum = _datums(datum_str)
    links = {'link_back': _link_back(datum), 'link_forward': _link_forward(datum)}

    weer = weather.Weather().from_gae(locatie=locatie.upper(), datum=datum)
    return flask.render_template('locatie.tpl', weer=weer, datum=datum, links=links)

@app.route('/regio/<regio>')
def regio_redirect(regio):
    if (mytime.datetime.today().hour < 20):
        return flask.redirect('/regio/%(regio)s/vandaag' % {'regio': regio}, 302)
    else:
        return flask.redirect('/regio/%(regio)s/morgen' % {'regio': regio}, 302)

@app.cache.memoize(timeout=60*5)
@app.route('/regio/<regio>/<datum_str>')
def regio(regio, datum_str = 'vandaag'):
    # Does the regio exist?
    regio = weather.Region.by_id(regio.lower())
    if not regio:
        return flask.abort(404)

    # Change input to real date object
    datum = _datums(datum_str)

    weer = weather.Weather().from_gae(regio=regio, datum=datum)
    return flask.render_template('regio.tpl', weer=weer, regio=regio, datum=datum, links=links)

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
    return str(controllers.tasks.wunderground.forecasts.hourly('zeeland'))

@app.route('/tasks/wunderground/forecasts/daily')
def tasks_wunderground_forecasts_daily():
    return str(controllers.tasks.wunderground.forecasts.daily('zeeland'))

@app.route('/tasks/regeneratecijfers')
def tasks_regeneratecijfers():
    for dbForecast in models.Forecast.all():
        forecast = weather.Forecast.from_gae(dbForecast)
        dbForecast.cijfer = forecast.generate_cijfer()
        dbForecast.put()

    return 'OK'

@app.route('/tasks/removeprobability')
def tasks_removeprobability():
    dbForecasts = models.Forecast.gql("WHERE probability_order > 1") 
    for dbForecast in dbForecasts:
        dbForecast.delete()

    return 'OK'

@app.route('/tasks/set_zeeland_to_station')
def set_zeeland_to_station():
    dbForecasts = models.Forecast.gql("WHERE locatie = 'zeeland'") 
    for dbForecast in dbForecasts:
        dbForecast.locatie = 'IZEELAND16'
        dbForecast.put()

    return 'OK'

@app.route('/test_cijfers')
def test_cijfers():
    gegevens = {}
    for temp in range(0, 36, 3):
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

    return flask.render_template('test_cijfers.tpl', gegevens=gegevens)

@app.route('/stations')
def stations():
    return str(weather.Region.by_id('zeeland'))
