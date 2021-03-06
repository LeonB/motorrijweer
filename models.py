from google.appengine.ext import db

class Forecast(db.Model):
    datapunt_van = db.DateTimeProperty(auto_now_add=False, required=True)
    datapunt_tot = db.DateTimeProperty(auto_now_add=False, required=True)
    tijdstip_datapunt = db.DateTimeProperty(auto_now_add=False, required=True)
    station_id = db.StringProperty(required=True)
    weertype = db.StringProperty(required=True, indexed=False)
    omschrijving = db.StringProperty(required=True, indexed=False)
    temperatuur = db.FloatProperty(required=True, indexed=False)
    gevoelstemperatuur = db.FloatProperty(required=True, indexed=False)
    neerslagkans = db.FloatProperty(required=True, indexed=False)
    neerslag_in_mm = db.FloatProperty(required=True, indexed=False)
    winterse_neerslag_in_mm = db.FloatProperty(default=0.0, required=False, indexed=False)
    bewolking = db.FloatProperty(required=True, indexed=False)
    windkracht = db.FloatProperty(required=True, indexed=False)
    windrichting = db.StringProperty(required=True, indexed=False)
    cijfer = db.FloatProperty(required=True, indexed=False)