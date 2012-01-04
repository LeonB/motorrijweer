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
import filters

@app.before_request
def before_request():
    app.timezone = flaskext.babel.get_timezone()

@app.errorhandler(404)
def page_not_found(e):
    return flask.render_template('404.tpl'), 404

@app.route('/')
def index():
    return flask.render_template('index.tpl')

@app.route('/<regio>')
#@app.cache.memoize()
def regio(regio):
    if regio not in app.config['LOCATIES'].keys():
        return flask.abort(404)

    weer = weather.Weather().from_gae(regio)
    today = mytime.datetime.today().date()
    #return str(len(weer.today.forecasts))
    #return str(weer.forecasts[-1].tijdstip_datapunt)
    #return str(len(weer.forecasts))
    #return str(weer.gevoelstemperatuur)
    return flask.render_template('index.tpl', weer=weer)

@app.route('/tasks/wunderground/forecasts/hourly')
def tasks_wunderground_forecasts_hourly():
    return controllers.tasks.wunderground.forecasts.hourly()

@app.route('/tasks/wunderground/forecasts/daily')
def tasks_wunderground_forecasts_daily():
    return controllers.tasks.wunderground.forecasts.daily()

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

@app.route('/test_cijfers')
def test_cijfers():
    gegevens = {}
    for temp in range(0, 36, 3):
        for neerslag_in_mm in range(0, 11, 1):
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

