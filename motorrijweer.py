import flask
import flaskext
from flaskext.cache import Cache
from flaskext.babel import Babel
from jinja2.ext import loopcontrols

# First set up app + cache (it may be used by other modules)
app = flask.Flask(__name__)
app.config.from_pyfile('motorrijweer.nl.cfg')
app.debug = True
app.cache = Cache(app)
app.babel = Babel(app)

import weather
import models
import mytime

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

@app.route('/tasks/wunderground/forecasts')
def tasks_wunderground_forecasts():
    now = mytime.datetime.now()
    #return str(app.config['LOCATIES']['zeeland'])

    # Make sure it is never request more than once every 15 minutes
    kwartier = now - mytime.timedelta(seconds=60*15)
    last_forecast = models.Forecast.gql("WHERE locatie = :locatie AND \
                        tijdstip_datapunt > :kwartier AND provider = 'wunderground'", 
                        locatie='zeeland', kwartier=kwartier).get()
    #return str(now)
    #if last_forecast:
        #last_forecast = weather.Forecast.from_gae(last_forecast)
        #return str(last_forecast.tijdstip_datapunt)

    for forecast in weather.Weather.from_wunderground('zeeland', days=3).forecasts:
        old_result = models.Forecast.gql("WHERE locatie = :locatie AND provider = 'wunderground' AND datapunt_van = :datapunt_van AND datapunt_tot = :datapunt_tot",
                                          locatie='zeeland',
                                          datapunt_van=forecast.datapunt_van,
                                          datapunt_tot=forecast.datapunt_tot).get()

        if old_result:
            old_result.weertype = forecast.weertype
            old_result.omschrijving = forecast.omschrijving
            old_result.temperatuur = forecast.temperatuur
            old_result.gevoelstemperatuur = forecast.gevoelstemperatuur
            old_result.neerslagkans = forecast.neerslagkans
            old_result.neerslag_in_mm = forecast.neerslag_in_mm
            old_result.bewolking = forecast.bewolking
            old_result.zonkans = forecast.zonkans
            old_result.windkracht = forecast.windkracht
            old_result.cijfer = forecast.cijfer
            old_result.put()
        else:
            dp = models.Forecast(
                datapunt_van = forecast.datapunt_van,
                datapunt_tot = forecast.datapunt_tot,
                tijdstip_datapunt = now,
                locatie = 'zeeland',
                weertype = forecast.weertype,
                omschrijving = forecast.omschrijving,
                temperatuur = forecast.temperatuur,
                gevoelstemperatuur = forecast.gevoelstemperatuur,
                neerslagkans = forecast.neerslagkans,
                neerslag_in_mm = forecast.neerslag_in_mm,
                bewolking = forecast.bewolking,
                zonkans = forecast.zonkans,
                windkracht = forecast.windkracht,
                windrichting = forecast.windrichting,
                cijfer = forecast.cijfer,
                provider = 'wunderground',
                probability_order = 0,
            )
            dp.put()

        # Oude resultaten updaten
        old_results = models.Forecast.gql("WHERE locatie = :locatie AND provider = 'wunderground' AND datapunt_van = :datapunt_van AND datapunt_tot = :datapunt_tot",
                                          locatie='zeeland',
                                          datapunt_van=forecast.datapunt_van,
                                          datapunt_tot=forecast.datapunt_tot)
        for result in old_results:
            result.probability_order += 1
            result.put()


    return 'OK'

@app.route('/tasks/regeneratecijfers')
def tasks_regeneratecijfers():
    for dbForecast in models.Forecast.all():
        forecast = weather.Forecast.from_gae(dbForecast)
        dbForecast.cijfer = forecast.generate_cijfer()
        dbForecast.put()

    return 'OK'

@app.route('/test_cijfers')
def test_cijfers():

    #return str(weather.Beaufort.from_kmh(55.5))
    #forecast = weather.Forecast()
    #return str(forecast.cijfer_windkracht(20))
    #forecast = weather.Forecast()
    #forecast.temperatuur = 7.0
    #forecast.windkracht = 20.0
    #forecast.neerslag_in_mm = 2.0
    #forecast.neerslagkans = 1
    #return str([forecast.cijfer_neerslagkans(forecast.neerslagkans)+ forecast.cijfer_neerslag_in_mm(forecast.neerslag_in_mm)])

    #gegevens = {}
    #for temp in range(0, 36, 3):
        #for neerslagkans in range(0, 110, 10):
            ##neerslagkans = float(neerslagkans)/100
            #for windkracht in range(0, 11, 1):
                #if not gegevens.has_key(temp):
                    #gegevens[temp] = {}
                #if not gegevens[temp].has_key(neerslagkans):
                    #gegevens[temp][neerslagkans] = {}
                #if not gegevens[temp][neerslagkans].has_key(windkracht):
                    #gegevens[temp][neerslagkans][windkracht] = []
                
                #obj = weather.Forecast()
                #obj.temperatuur = temp
                #obj.neerslagkans = float(neerslagkans)/100
                #obj.windkracht = windkracht
                #obj.neerslag_in_mm = 2.0
                ##obj.cijfer = obj.generate_cijfer()
                #gegevens[temp][neerslagkans][windkracht].append(obj)

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

