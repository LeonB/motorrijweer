import urllib2
import json
import math
import mytime
from motorrijweer import app
from collections import OrderedDict
import models
import xml.etree.ElementTree
import werkzeug
import copy

class Underground(object):
    def get_station(self, station, days=3):
        sf = None
        url = None
        feature = None

        if days == 3 :
            feature = 'hourly'
        elif days == 7:
            feature = 'hourly7day'
        else:
            raise Exception("I don't know how many days!")

        url = 'http://api.wunderground.com/api/%(api_key)s/%(feature)s/lang:NL/q/%(station)s.json?c=NL'
        try:
            sf = urllib2.urlopen(url % {'api_key': app.config['API_KEY'], 'feature': feature, 'station': station.code})
            json_string = sf.read()
        finally:
            if sf: sf.close()
        return json_string

class ForecastCollection(object):
    def __init__(self):
        self.forecasts = []
        self.now =  mytime.datetime.today()

    def to_forecast(self):
        forecast = Forecast()
        forecast.weertype = self.weertype
        forecast.omschrijving = self.omschrijving
        forecast.temperatuur = self.temperatuur
        forecast.gevoelstemperatuur = self.gevoelstemperatuur
        forecast.neerslagkans = self.neerslagkans
        forecast.neerslag_in_mm = self.neerslag_in_mm
        forecast.winterse_neerslag_in_mm = self.winterse_neerslag_in_mm
        forecast.bewolking = self.bewolking
        forecast.zonkans = self.zonkans
        forecast.windkracht = self.windkracht
        forecast.windrichting = self.windrichting
        forecast.cijfer = self.cijfer
        return forecast

    @property
    def today(self):
        today = mytime.datetime.today().date()
        gegevens_today = ForecastCollection()

        for forecast in self.forecasts:
            dt = forecast.datapunt_van
            if dt.date() == today:
                gegevens_today.forecasts.append(forecast)

        return gegevens_today

    @property
    def tomorrow(self):
        tomorrow = (mytime.datetime.today() + mytime.timedelta(days=1)).date()
        gegevens_tomorrow = ForecastCollection()

        for forecast in self.forecasts:
            dt = forecast.datapunt_van
            if dt.date() == tomorrow:
                gegevens_tomorrow.forecasts.append(forecast)

        return gegevens_tomorrow

    @property
    def overdag(self):
        gegevens_overdag = ForecastCollection()

        for forecast in self.forecasts:
            dt = forecast.datapunt_van
            if dt.hour >= 6 and dt.hour < 23:
                gegevens_overdag.forecasts.append(forecast)

        return gegevens_overdag

    @property
    def dagdelen(self):
        dagdelen = OrderedDict()
        dagdelen['ochtend'] = self.ochtend
        dagdelen['middag'] = self.middag
        dagdelen['avond'] = self.avond
        return dagdelen

    @property
    def per_uur(self):
        uren = {}

        for forecast in self.forecasts:
            dt = forecast.datapunt_van
            if not dt.hour in uren:
                uren[dt.hour] = ForecastCollection()
            uren[dt.hour].forecasts.append(forecast)

        return uren.values()

    @property
    def stations(self):
        stations = {}

        for forecast in self.forecasts:
            station_id = forecast.station_id
            if not station_id in stations:
                stations[station_id] = Station.by_id(station_id)
            stations[station_id].forecasts.append(forecast)

        return stations.values()

    @property
    def ochtend(self):
        gegevens_ochtend = ForecastCollection()

        for forecast in self.forecasts:
            dt = forecast.datapunt_van
            if dt.hour >= 6 and dt.hour < 12: #dus 16:59 telt. 17:00 niet
                gegevens_ochtend.forecasts.append(forecast)

        return gegevens_ochtend

    @property
    def middag(self):
        gegevens_middag = ForecastCollection()

        for forecast in self.forecasts:
            dt = forecast.datapunt_van
            if dt.hour >= 12 and dt.hour < 17: #dus 16:59 telt. 17:00 niet
                gegevens_middag.forecasts.append(forecast)

        return gegevens_middag

    @property
    def avond(self):
        gegevens_avond = ForecastCollection()

        for forecast in self.forecasts:
            dt = forecast.datapunt_van
            if dt.hour >= 17 and dt.hour < 23:
                gegevens_avond.forecasts.append(forecast)

        return gegevens_avond

    @property
    def last_update(self):
        last_update = None

        for forecast in self.forecasts:
            if not last_update or forecast.tijdstip_datapunt > last_update:
                last_update = forecast.tijdstip_datapunt

        return last_update

    ####### WEERGEGEVENS #######

    @property
    def droog_tot(self):
        droog_tot = None
        for forecast in self.forecasts:
            if forecast.neerslag_in_mm > 0.0:
                break
            else:
                droog_tot = forecast.datapunt_tot

        return droog_tot

    @property
    def droog_om(self):
        droog_om = None
        for forecast in self.forecasts:
            if forecast.neerslag_in_mm > 0.0:
                continue
            else:
                droog_om = forecast.datapunt_van
                break

        return droog_om

    @property
    def droge_periodes(self):
        droge_periodes = []
        droge_periode = None
        
        for forecast in self.forecasts:
            if forecast.neerslag_in_mm > 0.0:
                if droge_periode:
                    droge_periodes.append(droge_periode)
                    droge_periode = None
                else:
                    continue
            else: #dry period
                if not droge_periode:
                    droge_periode = ForecastCollection()
                    droge_periode.forecasts.append(forecast)
                else:
                    droge_periode.forecasts.append(forecast)

        if droge_periode:
            droge_periodes.append(droge_periode)

        return droge_periodes

    @property
    def weertype(self):
        if len(self.forecasts) == 0:
            return None

        weertypes = {}
        for forecast in self.forecasts:
            if not weertypes.has_key(forecast.weertype):
                weertypes[forecast.weertype] = 1
            else:
                weertypes[forecast.weertype] =+ 1

        #Counter.most_common zou ook werken?
        return sorted(weertypes, key=weertypes.get, reverse=True)[0]

    @property
    def omschrijving(self):
        if len(self.forecasts) == 0:
            return None

        omschrijvingen = {}
        for forecast in self.forecasts:
            if not omschrijvingen.has_key(forecast.omschrijving):
                omschrijvingen[forecast.omschrijving] = 1
            else:
                omschrijvingen[forecast.omschrijving] =+ 1

        return sorted(omschrijvingen, key=omschrijvingen.get, reverse=True)[0]

    @property
    def minimumtemperatuur(self):
        if len(self.forecasts) == 0:
            return None

        temperatuur = 100
        for forecast in self.forecasts:
            if forecast.temperatuur < temperatuur:
                temperatuur = forecast.temperatuur
        return temperatuur

    @property
    def maximumtemperatuur(self):
        if len(self.forecasts) == 0:
            return None

        temperatuur = -100
        for forecast in self.forecasts:
            if forecast.temperatuur > temperatuur:
                temperatuur = forecast.temperatuur
        return temperatuur

    @property
    def temperatuur(self):
        if len(self.forecasts) == 0:
            return None

        temperatuur = 0.0
        for forecast in self.forecasts:
            temperatuur += forecast.temperatuur

        temperatuur = temperatuur/len(self.forecasts)
        return temperatuur

    @property
    def gevoelstemperatuur(self):
        if len(self.forecasts) == 0:
            return None

        gevoelstemperatuur = 0.0
        for forecast in self.forecasts:
            gevoelstemperatuur += forecast.gevoelstemperatuur

        gevoelstemperatuur = gevoelstemperatuur/len(self.forecasts)
        return gevoelstemperatuur

    @property
    def neerslagkans(self):
        if len(self.forecasts) == 0:
            return None

        neerslagkans = 0.0
        for forecast in self.forecasts:
            neerslagkans += forecast.neerslagkans
        neerslagkans = neerslagkans/len(self.forecasts)

        if neerslagkans > 1.0:
            return 1.0

        return neerslagkans

    @property
    def neerslag_in_mm(self):
        if len(self.forecasts) == 0:
            return None

        neerslag_in_mm = 0.0
        for forecast in self.forecasts:
            neerslag_in_mm += forecast.neerslag_in_mm

        neerslag_in_mm = neerslag_in_mm/len(self.forecasts)
        return neerslag_in_mm

    @property
    def winterse_neerslag_in_mm(self):
        if len(self.forecasts) == 0:
            return None

        winterse_neerslag_in_mm = 0.0
        for forecast in self.forecasts:
            winterse_neerslag_in_mm += forecast.winterse_neerslag_in_mm

        winterse_neerslag_in_mm = winterse_neerslag_in_mm/len(self.forecasts)
        return winterse_neerslag_in_mm

    @property
    def bewolking(self):
        if len(self.forecasts) == 0:
            return None

        bewolking = 0.0
        for forecast in self.forecasts:
            bewolking += forecast.bewolking

        bewolking = bewolking/len(self.forecasts)
        return bewolking

    @property
    def zonkans(self):
        if len(self.forecasts) == 0:
            return None

        zonkans = 0.0
        for forecast in self.forecasts:
            zonkans += forecast.zonkans

        zonkans = zonkans/len(self.forecasts)
        return zonkans

    @property
    def windkracht(self):
        if len(self.forecasts) == 0:
            return None

        windkracht = 0.0
        for forecast in self.forecasts:
            windkracht += forecast.windkracht

        windkracht = windkracht/len(self.forecasts)
        return windkracht

    @property
    def windrichting(self):
        if len(self.forecasts) == 0:
            return None

        windrichtingen = {}
        for forecast in self.forecasts:
            if not windrichtingen.has_key(forecast.windrichting):
                windrichtingen[forecast.windrichting] = 1
            else:
                windrichtingen[forecast.windrichting] =+ 1

        if len(windrichtingen) == 0:
            return None

        windrichtingen = sorted(windrichtingen)
        windrichtingen.reverse()
        return windrichtingen[0]

    @property
    def cijfer(self):
        if len(self.forecasts) == 0:
            return None

        cijfer = 0.0
        for forecast in self.forecasts:
            cijfer += forecast.cijfer

        cijfer = cijfer/len(self.forecasts)
        return cijfer

    def deelcijfers(self):
        if len(self.forecasts) > 0:
            return self.to_forecast().deelcijfers()
        else:
            return {}

class Weather(object):

    @classmethod
    def from_wunderground(cls, station, days=3):
        collection = ForecastCollection()
        u = Underground()
        json_string = u.get_station(station, days=days)
        parsed_json = json.loads(json_string)

        for hourly_forecast in parsed_json['hourly_forecast']:
            #hour = hourly_forecast['FCTTIME']['hour'] + ':' + hourly_forecast['FCTTIME']['min']
            forecast = Forecast()
            forecast.bind(hourly_forecast)
            collection.forecasts.append(forecast)

        return collection

    @classmethod
    def has_datapunten(cls, station = None, regio = None, provincie = None, datum = None):
        stations = []
        if station:
            stationss = [station]
        elif regio:
            stations = map(lambda x: x.id, regio.stations)
        elif provincie:
            for regio in provincie.regios:
                stations = stations + map(lambda x: x.id, regio.stations)

        datum_van = mytime.datetime(datum.year, datum.month, datum.day, 6)
        datum_tot = mytime.datetime(datum.year, datum.month, datum.day, 23)

        query = models.Forecast.all()
        query.filter('station_id IN', stations)
        query.filter('datapunt_van >=', datum_van)
        query.filter('datapunt_van <', datum_tot)
        #query.order('datapunt_van')
        return query.count(limit=17)

    @classmethod
    def from_gae(cls, station = None, regio = None, provincie = None, datum = None):
        stations = []
        if station:
            stations = [station.id]
        elif regio:
            stations = map(lambda x: x.id, regio.stations)
        elif provincie:
            stations = stations + map(lambda x: x.id, provincie.stations)

        collection = ForecastCollection()

        if len(stations) == 0:
            return collection

        dbForecasts = models.Forecast.gql("WHERE station_id IN :stations AND datapunt_van >= :datum \
                                          AND datapunt_van < :plus_dag \
                                          ORDER BY datapunt_van ASC",
                                          stations=stations,
                                          datum=datum,
                                          plus_dag=datum + mytime.timedelta(days=1),
                                          min_dag=datum - mytime.timedelta(days=1))

        #dbForecasts = sorted(dbForecasts, key=lambda x: x.tijdstip_datapunt, reverse=True)
        for dbForecast in dbForecasts:
            forecast = Forecast.from_gae(dbForecast)

            #if len(collection.forecasts) > 0:
                #previous_forecast = collection.forecasts[-1]
                #if previous_forecast.datapunt_van > forecast.datapunt_van:
                    #break

            collection.forecasts.append(forecast)

        return collection

class Forecast(object):

    def __init__(self):
        self.datapunt_van = None
        self.datapunt_tot = None
        self.tijdstip_datapunt = None
        self.station_id = None
        self.weertype = None
        self.omschrijving = None
        self.temperatuur = None
        self.minimumtemperatuur = None
        self.maximumtemperatuur = None
        self.gevoelstemperatuur = None
        self.neerslagkans = None
        self.neerslag_in_mm = None
        self.winterse_neerslag_in_mm = None
        self.bewolking = None
        self.zonkans = None
        self.windkracht = None
        self.windrichting = None
        self.cijfer = None

    @classmethod
    def from_gae(cls, gae_obj):
        forecast = Forecast()

        forecast.datapunt_van = mytime.datetime.from_utc(gae_obj.datapunt_van)
        forecast.datapunt_tot = mytime.datetime.from_utc(gae_obj.datapunt_tot)
        forecast.tijdstip_datapunt = mytime.datetime.from_utc(gae_obj.tijdstip_datapunt)
        forecast.station_id = gae_obj.station_id
        forecast.weertype = gae_obj.weertype
        forecast.omschrijving = gae_obj.omschrijving
        forecast.temperatuur = gae_obj.temperatuur
        forecast.gevoelstemperatuur = gae_obj.gevoelstemperatuur
        forecast.neerslagkans = gae_obj.neerslagkans
        forecast.neerslag_in_mm = gae_obj.neerslag_in_mm
        forecast.winterse_neerslag_in_mm = gae_obj.winterse_neerslag_in_mm
        forecast.bewolking = gae_obj.bewolking
        forecast.zonkans = 1 - forecast.bewolking
        forecast.windkracht = gae_obj.windkracht
        forecast.windrichting = gae_obj.windrichting
        forecast.cijfer = gae_obj.cijfer
        #forecast.cijfer = forecast.generate_cijfer() #niet uit de db halen

        return forecast

    def bind(self, gegevens):
        self.datapunt_van = mytime.datetime.fromtimestamp(float(gegevens['FCTTIME']['epoch']))
        self.datapunt_tot = self.datapunt_van + mytime.timedelta(seconds=60*60)
        self.tijdstip_datapunt = mytime.datetime.now()
        self.weertype = gegevens['icon']
        self.omschrijving = gegevens['condition']
        self.temperatuur = float(gegevens['temp']['metric'])
        self.gevoelstemperatuur = float(gegevens['feelslike']['metric'])
        self.neerslagkans = float(gegevens['pop'])/100
        try:
            self.winterse_neerslag_in_mm = float(gegevens['snow']['metric'])
        except ValueError:
            self.winterse_neerslag_in_mm = 0.0
        try:
            self.neerslag_in_mm = float(gegevens['qpf']['metric'])
        except ValueError:
            self.neerslag_in_mm = 0.0
        try:
            self.bewolking = float(gegevens['sky'])/100
        except ValueError:
            self.bewolking = 0.0
        self.zonkans = 1 - self.bewolking
        self.windkracht = float(gegevens['wspd']['metric'])
        self.windrichting = gegevens['wdir']['dir']

    def normpdf(self, x, mu, sigma):
        x = float(x)
        mu = float(mu)
        sigma = float(sigma)
        u = (x-mu)/abs(sigma)
        y = (1/(math.sqrt(2*math.pi)*abs(sigma)))*math.exp(-u*u/2)
        return y

    #@property
    def deelcijfers(self):
        return {
            'temperatuur': self.cijfer_temperatuur(self.temperatuur),
            #'neerslagkans': self.cijfer_neerslagkans(self.neerslagkans),
            'neerslag_in_mm': self.cijfer_neerslag_in_mm(self.neerslag_in_mm),
            'windkracht': self.cijfer_windkracht(Beaufort.from_kmh(self.windkracht)),
            'winterse_neerslag_in_mm': self.cijfer_winterse_neerslag_in_mm(self.winterse_neerslag_in_mm),
            'bewolking': self.cijfer_bewolking(self.bewolking),
        }

    def generate_cijfer(self):
        cijfer = 0.0
        for deelcijfer in self.deelcijfers().values():
            cijfer += deelcijfer

        if cijfer < 0:
            return 0.0

        if cijfer > 10:
            return 10.0

        return cijfer

    def cijfer_temperatuur(self, i):
        best = 23
        afwijking = 8
        baseline = self.normpdf(best, best, afwijking)
        max_punten = 3
        mod = max_punten/baseline
        i1 = self.normpdf(i, best, afwijking)*mod

        worst = -10
        afwijking = 5
        baseline = self.normpdf(worst, worst, afwijking)
        max_punten = -3
        mod = max_punten/baseline
        i2 = self.normpdf(i, worst, afwijking)*mod

        return i1+i2

    def cijfer_neerslagkans(self, i):
        best = 0
        afwijking = 0.3 #30/100
        baseline = self.normpdf(best, best, afwijking)
        max_punten = 0
        mod = max_punten/baseline
        return self.normpdf(i, best, afwijking)*mod

    def cijfer_neerslag_in_mm(self, i):
        best = 0
        afwijking = 0.15 #neerslag in 1 uur
        baseline = self.normpdf(best, best, afwijking)
        max_punten = 4
        mod = max_punten/baseline
        return self.normpdf(i, best, afwijking)*mod

    def cijfer_windkracht(self, i):
        """boven de 20 graden gaat wind positief meetellen. Daaronder negatief.
        >= windkracht 7 zijn minpunten (altijd). """
        if self.temperatuur < 23:
            best = 0
            afwijking = 4
            baseline = self.normpdf(best, best, afwijking)
            max_punten = 3
            mod = max_punten/baseline
            i1 = self.normpdf(i, best, afwijking)*mod

            worst = 12
            afwijking = 4
            baseline = self.normpdf(worst, worst, afwijking)
            max_punten = -3
            mod = max_punten/baseline
            i2 = self.normpdf(i, worst, afwijking)*mod

            return i1+i2
        else:
            best = 3
            afwijking = 2.5
            baseline = self.normpdf(best, best, afwijking)
            max_punten = 3
            mod = max_punten/baseline
            i1 = self.normpdf(i, best, afwijking)*mod

            worst = 12
            afwijking = 4
            baseline = self.normpdf(worst, worst, afwijking)
            max_punten = -3
            mod = max_punten/baseline
            i2 = self.normpdf(i, worst, afwijking)*mod

            return i1+i2

    def cijfer_winterse_neerslag_in_mm(self, i):
        if i > 0:
            return -2

        return 0

    def cijfer_bewolking(self, i):
        worst = 1 #hele dag bewolking
        afwijking = 0.425
        baseline = self.normpdf(worst, worst, afwijking)
        max_punten = -0.5 #max 0.5 punten aftrek (i=1)
        mod = max_punten/baseline
        return self.normpdf(i, worst, afwijking)*mod


class Beaufort(object):
    omschrijvingen = {
        0: 'Stil',
        1: 'Zwak',
        2: 'Zwak',
        3: 'Matig',
        4: 'Matig',
        5: 'Vrij krachtig',
        6: 'Krachtig',
        7: 'Hard',
        8: 'Stormachtig',
        9: 'Storm',
        10: 'Zware storm',
        11: 'Zeer zware storm / orkaanachtig',
        12: 'Orkaan',
    }

    data = {
        0: 0,
        1: 1,
        2: 6,
        3: 12,
        4: 20,
        5: 29,
        6: 39,
        7: 50,
        8: 62,
        9: 75,
        10: 89,
        11: 103,
        12: 117,
    }

    @classmethod
    def from_kmh(cls, i):
        for beaufort, kmh in cls.data.items():
            if kmh > i:
                return beaufort-1
        # else
        return cls.data.keys()[-1]

    @classmethod
    def from_beaufort(cls, i):
        for beaufort, kmh in cls.data.items():
            if beaufort == i:
                kmh_1 = cls.data[beaufort]
                kmh_2 = cls.data[beaufort+1]-1
                return (kmh_1, kmh_2)

class Provincie(object):
    provincies_cache = None

    def __init__(self):
        self.regios = []

    @classmethod
    def all(cls):
        # cls.provincies_cache = None
        if not cls.provincies_cache:
            et = xml.etree.ElementTree.parse('stations.xml')
            provincies = []

            for xmlProvincie in et.findall('provincie'):
                provincie = Provincie()
                provincie.id = xmlProvincie.find('id').text
                provincie.name = xmlProvincie.find('name').text
                provincies.append(provincie)

                for xmlRegio in xmlProvincie.find('regios').findall('regio'):
                    regio = Regio()
                    regio.id = xmlRegio.find('id').text
                    regio.name = xmlRegio.find('name').text
                    regio.provincie = provincie
                    provincie.regios.append(regio)

                    stations = xmlRegio.find('stations')
                    if stations:
                        for xmlStation in stations.findall('station'):
                            station = Station()
                            station.id = xmlStation.find('id').text
                            station.code = xmlStation.find('code').text
                            station.name = xmlStation.find('name').text
                            station.coordinates = {}
                            station.coordinates['latitude'] = xmlStation.find('coordinates').find('latitude').text
                            station.coordinates['longitude'] = xmlStation.find('coordinates').find('longitude').text
                            station.provincie = provincie
                            station.regio = regio
                            regio.stations.append(station)

            cls.provincies_cache = provincies

        # return a copy of this object because it is going to be modified
        # and then it wil be stored in this class: so return a copy
        return copy.deepcopy(cls.provincies_cache)

    @classmethod
    def by_id(cls, provincie_id):
        provincies = Provincie.all()
        provincies = filter(lambda x: x.id == provincie_id, provincies)

        if len(provincies) == 0:
            return None

        return provincies[0]

    @property
    def stations(self):
        stations = []
        for regio in self.regios:
            for station in regio.stations:
                stations.append(station)

        return stations

class Regio(object):

    def __init__(self):
        self.stations = []
        self.provincie = None

    @classmethod
    def all(cls):
        regios = []
        for provincie in Provincie.all():
            for regio in provincie.regios:
                regios.append(regio)

        return regios

    @classmethod
    def by_id(cls, regio_id):
        regios = Regio.all()
        regios = filter(lambda x: x.id == regio_id, regios)

        if len(regios) == 0:
            return None

        return regios[0]


class Station(ForecastCollection):

    def __init__(self):
        ForecastCollection.__init__(self)
        self.provincie = None
        self.regio = None

    @classmethod
    def all(cls):
        stations = []
        for regio in Regio.all():
            for station in regio.stations:
                stations.append(station)

        return stations

    @classmethod
    def all_ids(cls):
        ids = []
        for station in cls.all():
            ids.append(station.id)

        return ids

    @classmethod
    def by_id(cls, station_id):
        stations = cls.all()
        stations = filter(lambda x: x.id == station_id, stations)

        if len(stations) == 0:
            return None

        return stations[0]
