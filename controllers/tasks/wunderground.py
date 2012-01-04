import mytime
import models
import weather

class forecasts(object):

    @classmethod
    def hourly(cls):
        now = mytime.datetime.now()
        #return str(app.config['LOCATIES']['zeeland'])

        # Make sure it is never request more than once every 15 minutes
        kwartier = now - mytime.timedelta(seconds=60*15)
        last_forecast = models.Forecast.gql("WHERE locatie = :locatie AND \
                            tijdstip_datapunt > :kwartier AND provider = 'wunderground'", 
                            locatie='zeeland', kwartier=kwartier).get()

        if last_forecast:
            last_forecast = weather.Forecast.from_gae(last_forecast)
            return str(last_forecast.tijdstip_datapunt)

        return cls._import_forecasts(days=3)

    @classmethod
    def daily(cls):
        return cls._import_forecasts(days=7)

    @classmethod
    def _import_forecasts(cls, days=3, hours_in_the_future_to_skip=None):
        now = mytime.datetime.now()

        #return str(len(weather.Weather.from_wunderground('zeeland', days=7).forecasts))
        for forecast in weather.Weather.from_wunderground('zeeland', days=days).forecasts:

            # evt: if van > 3 uur (ofzo): skippen

            old_result = models.Forecast.gql("WHERE locatie = :locatie AND provider = 'wunderground' AND datapunt_van = :datapunt_van AND datapunt_tot = :datapunt_tot",
                                              locatie='zeeland',
                                              datapunt_van=forecast.datapunt_van,
                                              datapunt_tot=forecast.datapunt_tot).get()

            if old_result:
                if old_result.weertype == forecast.weertype and \
                old_result.omschrijving == forecast.omschrijving and \
                old_result.temperatuur == forecast.temperatuur and \
                old_result.gevoelstemperatuur == forecast.gevoelstemperatuur and \
                old_result.neerslagkans == forecast.neerslagkans and \
                old_result.neerslag_in_mm == forecast.neerslag_in_mm and \
                old_result.bewolking == forecast.bewolking and \
                old_result.zonkans == forecast.zonkans and \
                old_result.windkracht == forecast.windkracht and \
                old_result.cijfer == forecast.cijfer:
                    continue

                old_result.tijdstip_datapunt = now
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

        return 'OK'

