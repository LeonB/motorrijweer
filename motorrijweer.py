import os
import flask
import flaskext
from flaskext.cache import Cache
from flaskext.babel import Babel

# First set up app + cache (it may be used by other modules)
app = flask.Flask(__name__)
app.config.from_pyfile('motorrijweer.nl.cfg')

# Check for Google appengine signature
if os.environ['SERVER_SOFTWARE'].startswith('Development'):
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
import helpers

@app.before_request
def before_request():
    app.timezone = flaskext.babel.get_timezone()
    app.jinja_env.globals['now'] = mytime.datetime.now()

@app.errorhandler(404)
def page_not_found(e):
    return flask.render_template('404.jinja'), 404

@app.route('/')
@app.cache.memoize(timeout=60*60*24) # 24 uur
@app.add_expires_header(minutes=60*24) # 24 uur
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

@app.route('/regio/<regio>/<datum_str>')
@app.cache.memoize(timeout=60*60*6) # 6 uur
@app.add_expires_header(minutes=60)
def regio(regio, datum_str = 'vandaag'):
    # Does the regio exist?
    regio = weather.Regio.by_id(regio.lower())
    if not regio:
        return flask.abort(404)

    # Change input to real date object
    datum = helpers.datums(datum_str)

    weer = weather.Weather().from_gae(regio=regio, datum=datum)
    return flask.render_template('regio.jinja', weer=weer, regio=regio, datum=datum)

## PROVINCIE ##
@app.route('/provincie/<provincie>')
def provincie_redirect(provincie):
    if (mytime.datetime.today().hour < 20):
        return flask.redirect('/provincie/%(provincie)s/vandaag' % {'provincie': provincie}, 302)
    else:
        return flask.redirect('/provincie/%(provincie)s/morgen' % {'provincie': provincie}, 302)

@app.route('/provincie/<provincie>/<datum_str>')
@app.cache.memoize(timeout=60*60*6) # 6 uur
@app.add_expires_header(minutes=60)
def provincie(provincie, datum_str = 'vandaag'):
    # Does the provincie exist?
    provincie = weather.Provincie.by_id(provincie.lower())
    if not provincie:
        return flask.abort(404)

    # Change input to real date object
    datum = helpers.datums(datum_str)

    weer = weather.Weather().from_gae(provincie=provincie, datum=datum)
    return flask.render_template('provincie.jinja', weer=weer, provincie=provincie, datum=datum)

##### TASKS #####

@app.route('/tasks/wunderground/forecasts/hourly')
def tasks_wunderground_forecasts_hourly():
    result = str(controllers.tasks.wunderground.forecasts.hourly())
    empty_cache()
    return result

@app.route('/tasks/wunderground/forecasts/daily')
def tasks_wunderground_forecasts_daily():
    result = str(controllers.tasks.wunderground.forecasts.daily())
    empty_cache()
    return result

@app.route('/tasks/delete_old_forecasts')
def tasks_delete_old_forecasts():
    dagen = 21
    datum = (mytime.datetime.today() + mytime.timedelta(days=-21)).date()
    for forecast in models.Forecast.gql('WHERE datapunt_van < :datum', datum=datum):
        forecast.delete()

    return 'OK'

@app.route('/tasks/regeneratecijfers')
def tasks_regeneratecijfers():
    for dbForecast in models.Forecast.all():
        forecast = weather.Forecast.from_gae(dbForecast)
        dbForecast.cijfer = forecast.generate_cijfer()
        dbForecast.put()

    return 'OK'

@app.route('/tasks/empty_cache')
def empty_cache():
    app.cache.cache.clear()
    app.cache._memoized = []
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

@app.route('/stations')
def stations():
    return str(weather.Region.by_id('zeeland'))

@app.route('/sitemap.xml')
@app.cache.memoize(timeout=60*60*24) # 24 uur
@app.add_content_type_header('text/xml')
def sitemap():
    url_root = flask.request.url_root[:-1]
    provincies = weather.Provincie.all()
    return flask.render_template('sitemap.jinja', url_root=url_root, provincies=provincies)