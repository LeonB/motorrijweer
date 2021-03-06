import mytime
import models
import weather

class forecasts(object):

    @classmethod
    def hourly(cls):
        retvals = []

        for station in weather.Station.all():
            now = mytime.datetime.now()

            # Make sure it is never request more than once every 30 minutes
            timediff = now - mytime.timedelta(seconds=60*30)
            last_forecast = models.Forecast.gql("WHERE station_id = :station_id AND \
                                tijdstip_datapunt > :timediff",
                                station_id=station.id, timediff=timediff).get()

            # There's already a forecast < 15 minutes: skip
            if last_forecast:
                continue

            # return it
            retvals.append(station)
        return retvals

    @classmethod
    def _import_forecasts(cls, station, days=3, hours_in_the_future_to_skip=None):
        now = mytime.datetime.now()

        winterse_neerslag = 0
        for forecast in weather.Weather.from_wunderground(station, days=days).forecasts:

            # checken op winterse neerslag in ALLE uren (ook de geskipte)
            if forecast.winterse_neerslag_in_mm:
                winterse_neerslag = 48
            elif forecast.winterse_neerslag_in_mm and winterse_neerslag:
                winterse_neerslag = winterse_neerslag - 1

            if winterse_neerslag:
                minpunten = 2.0
            else:
                minpunten = 0

            # optimalisatie om op datastore te besparen
            if forecast.datapunt_van.hour < 6:
                continue

            # optimalisatie om op datastore te besparen
            if forecast.datapunt_van.hour >= 23:
                continue

            old_result = models.Forecast.gql("WHERE station_id = :station_id AND datapunt_van = :datapunt_van AND datapunt_tot = :datapunt_tot",
                                              station_id=station.id,
                                              datapunt_van=forecast.datapunt_van,
                                              datapunt_tot=forecast.datapunt_tot).get()

            if old_result:
                if old_result.weertype == forecast.weertype and \
                old_result.omschrijving == forecast.omschrijving and \
                old_result.temperatuur == forecast.temperatuur and \
                old_result.gevoelstemperatuur == forecast.gevoelstemperatuur and \
                old_result.neerslagkans == forecast.neerslagkans and \
                old_result.neerslag_in_mm == forecast.neerslag_in_mm and \
                old_result.winterse_neerslag_in_mm == forecast.winterse_neerslag_in_mm and \
                old_result.bewolking == forecast.bewolking and \
                old_result.windkracht == forecast.windkracht and \
                old_result.cijfer == (forecast.generate_cijfer() - minpunten):
                    # alles is hetzelfde gebleven
                    # Moet ik de timestamp updaten?!?: nee, kost alleen maar writes
                    continue

                # Stond al in de db, maar geupdate resultaten
                old_result.tijdstip_datapunt = now
                old_result.weertype = forecast.weertype
                old_result.omschrijving = forecast.omschrijving
                old_result.temperatuur = forecast.temperatuur
                old_result.gevoelstemperatuur = forecast.gevoelstemperatuur
                old_result.neerslagkans = forecast.neerslagkans
                old_result.neerslag_in_mm = forecast.neerslag_in_mm
                old_result.winterse_neerslag_in_mm = forecast.winterse_neerslag_in_mm
                old_result.bewolking = forecast.bewolking
                old_result.windkracht = forecast.windkracht
                old_result.cijfer = (forecast.generate_cijfer() - minpunten)
                old_result.put()
                continue
            else:
                dp = models.Forecast(
                    datapunt_van = forecast.datapunt_van,
                    datapunt_tot = forecast.datapunt_tot,
                    tijdstip_datapunt = now,
                    station_id = station.id,
                    weertype = forecast.weertype,
                    omschrijving = forecast.omschrijving,
                    temperatuur = forecast.temperatuur,
                    gevoelstemperatuur = forecast.gevoelstemperatuur,
                    neerslagkans = forecast.neerslagkans,
                    neerslag_in_mm = forecast.neerslag_in_mm,
                    winterse_neerslag_in_mm = forecast.winterse_neerslag_in_mm,
                    bewolking = forecast.bewolking,
                    windkracht = forecast.windkracht,
                    windrichting = forecast.windrichting,
                    cijfer = (forecast.generate_cijfer() - minpunten),
                )
                dp.put()
                continue

        return 'OK'

