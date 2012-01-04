import urllib2
import json
import math
import mytime
from motorrijweer import app
from collections import OrderedDict
import models

class Underground(object):
    #@app.cache.cached()
    def get_region(self, region, days=3):
        sf = None
        try:
            if days == 3 :
                sf = urllib2.urlopen('http://api.wunderground.com/api/172be46581dbc68e/hourly/lang:NL/q/pws:IZEELAND16.json?c=NL')
            elif days == 7:
                sf = urllib2.urlopen('http://api.wunderground.com/api/172be46581dbc68e/hourly7day/lang:NL/q/pws:IZEELAND16.json?c=NL')
            else:
                raise Exception("I don't know how many days!")
            #sf = open('hourly_vlissingen.json')
            json = sf.read()
        finally:
            if sf: sf.close()
        return json

class ForecastCollection(object):
    def __init__(self):
        self.forecasts = []
        self.now =  mytime.datetime.today()

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

    def droge_periodes(self):
        pass

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
        #neerslagkans = neerslagkans/len(self.forecasts)

        if neerslagkans > 1.0:
            return 1.0

        return neerslagkans

    @property
    def neerslag_in_mm(self):
        if len(self.forecasts) == 0:
            return None

        neerslag_in_mm = 0.0
        for forecast in self.forecasts:
            neerslag_in_mm += (forecast.neerslag_in_mm*forecast.neerslagkans)
        return neerslag_in_mm

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
        #forecast = Forecast()
        #forecast.temperatuur = self.temperatuur
        #forecast.windkracht = self.windkracht
        #forecast.neerslagkans = self.neerslagkans
        #forecast.neerslag_in_mm = self.neerslag_in_mm
        #return forecast.generate_cijfer()

        if len(self.forecasts) == 0:
            return None

        cijfer = 0.0
        for forecast in self.forecasts:
            cijfer += forecast.cijfer

        cijfer = cijfer/len(self.forecasts)
        return cijfer

class Weather(object):

    @classmethod
    def from_wunderground(cls, region, days=3):
        collection = ForecastCollection()
        u = Underground()
        json_string = u.get_region(region, days=days)
        parsed_json = json.loads(json_string)

        for hourly_forecast in parsed_json['hourly_forecast']:
            #hour = hourly_forecast['FCTTIME']['hour'] + ':' + hourly_forecast['FCTTIME']['min']
            dt = mytime.datetime.fromtimestamp(int(hourly_forecast['FCTTIME']['epoch']))
            forecast = Forecast()
            forecast.bind(hourly_forecast) 
            collection.forecasts.append(forecast)

        return collection

    @classmethod
    def from_gae(cls, locatie):
        collection = ForecastCollection()
        begin_vandaag = mytime.datetime.today().date()
        dbForecasts = models.Forecast.gql("WHERE locatie = :locatie AND datapunt_van > :begin_vandaag \
                                          ORDER BY datapunt_van ASC", 
                                          locatie=locatie,
                                          begin_vandaag=begin_vandaag)

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
        datapunt_van = None
        datapunt_tot = None
        tijdstip_datapunt = None
        locatie = None
        weertype = None
        omschrijving = None
        temperatuur = None
        minimumtemperatuur = None
        maximumtemperatuur = None
        gevoelstemperatuur = None
        neerslagkans = None
        neerslag_in_mm = None
        bewolking = None
        zonkans = None
        windkracht = None
        windrichting = None
        cijfer = None

    @classmethod
    def from_gae(cls, gae_obj):
        forecast = Forecast()

        forecast.datapunt_van = mytime.datetime.from_utc(gae_obj.datapunt_van)
        forecast.datapunt_tot = mytime.datetime.from_utc(gae_obj.datapunt_tot)
        forecast.tijdstip_datapunt = mytime.datetime.from_utc(gae_obj.tijdstip_datapunt)
        forecast.locatie = gae_obj.locatie
        forecast.weertype = gae_obj.weertype
        forecast.omschrijving = gae_obj.omschrijving
        forecast.temperatuur = gae_obj.temperatuur
        forecast.gevoelstemperatuur = gae_obj.gevoelstemperatuur
        forecast.neerslagkans = gae_obj.neerslagkans
        forecast.neerslag_in_mm = gae_obj.neerslag_in_mm
        forecast.bewolking = gae_obj.bewolking
        forecast.zonkans = gae_obj.zonkans
        forecast.windkracht = gae_obj.windkracht
        forecast.windrichting = gae_obj.windrichting
        forecast.cijfer = gae_obj.cijfer

        return forecast

    def bind(self, gegevens):
        self.datapunt_van = mytime.datetime.fromtimestamp(float(gegevens['FCTTIME']['epoch']))
        self.datapunt_tot = self.datapunt_van + mytime.timedelta(seconds=60*60)
        self.tijdstip_datapunt = mytime.datetime.now()
        self.weertype = gegevens['icon']
        self.omschrijving = gegevens['condition']
        self.temperatuur = float(gegevens['temp']['metric'])
        # minimumtemperatuur (samenvoegen uit verschillende weerstations?)
        # maximumtemperatuur (idem)
        self.gevoelstemperatuur = float(gegevens['feelslike']['metric'])
        self.neerslagkans = float(gegevens['pop'])/100
        self.neerslag_in_mm = float(gegevens['qpf']['metric'])
        self.bewolking = float(gegevens['sky'])/100
        self.zonkans = 1 - self.bewolking
        self.windkracht = float(gegevens['wspd']['metric'])
        self.windrichting = gegevens['wdir']['dir']
        self.cijfer = self.generate_cijfer()

    def normpdf(self, x, mu, sigma):
        x = float(x)
        mu = float(mu)
        sigma = float(sigma)
        u = (x-mu)/abs(sigma)
        y = (1/(math.sqrt(2*math.pi)*abs(sigma)))*math.exp(-u*u/2)
        return y
    
    #@property
    #def cijfer(self):
        #return self.generate_cijfer()

    def generate_cijfer(self):
        #self.temperatuur = 12
        #self.neerslagkans = 0.2
        #self.windkracht = 4

        cijfer = 0.0
        cijfer += self.cijfer_temperatuur(self.temperatuur)
        cijfer += self.cijfer_neerslagkans(self.neerslagkans)
        cijfer += self.cijfer_neerslag_in_mm(self.neerslag_in_mm)
        cijfer += self.cijfer_windkracht(Beaufort.from_kmh(self.windkracht))

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
        return self.normpdf(i, best, afwijking)*mod

    def cijfer_neerslagkans(self, i):
        best = 0
        afwijking = 0.3 #30/100
        baseline = self.normpdf(best, best, afwijking)
        max_punten = 0
        mod = max_punten/baseline
        return self.normpdf(i, best, afwijking)*mod

    def cijfer_neerslag_in_mm(self, i):
        best = 0
        afwijking = 3
        baseline = self.normpdf(best, best, afwijking)
        max_punten = 4
        mod = max_punten/baseline
        return self.normpdf(i, best, afwijking)*mod

    #def cijfer_windkracht(self, i):
        #"""boven de 20 graden gaat wind positief meetellen. Daaronder negatief. 
        #>= windkracht 7 zijn minpunten (altijd). """
        #i = int(i)
        #if i < 7:
            #if self.temperatuur < 23:
                #best = 0
                #afwijking = 4
                #baseline = self.normpdf(best, best, afwijking)
                #max_punten = 3
                #mod = max_punten/baseline
                #return self.normpdf(i, best, afwijking)*mod
            #else:
                #best = 3
                #afwijking = 2.5
                #baseline = self.normpdf(best, best, afwijking)
                #max_punten = 3
                #mod = max_punten/baseline
                #return self.normpdf(i, best, afwijking)*mod
        #else:
            #worst = 12
            #afwijking = 1.5
            #baseline = self.normpdf(worst, worst, afwijking)
            #max_punten = -3
            #mod = max_punten/baseline
            #return self.normpdf(i, worst, afwijking)*mod

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
