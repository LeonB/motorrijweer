from google.appengine.ext import db

class Forecast(db.Model):
    datapunt_van = db.DateTimeProperty(auto_now_add=False, required=True)
    datapunt_tot = db.DateTimeProperty(auto_now_add=False, required=True)
    tijdstip_datapunt = db.DateTimeProperty(auto_now_add=False, required=True)
    locatie = db.StringProperty(required=True) #zeeland, noord-brabant
    weertype = db.StringProperty(required=True, indexed=False)
    omschrijving = db.StringProperty(required=True, indexed=False)
    temperatuur = db.FloatProperty(required=True, indexed=False)
    #minimumtemperatuur = db.FloatProperty()
    #maximumtemperatuur = db.FloatProperty()
    gevoelstemperatuur = db.FloatProperty(required=True, indexed=False)
    neerslagkans = db.FloatProperty(required=True, indexed=False)
    neerslag_in_mm = db.FloatProperty(required=True, indexed=False)
    bewolking = db.FloatProperty(required=True, indexed=False)
    zonkans = db.FloatProperty(required=True, indexed=False)
    windkracht = db.FloatProperty(required=True, indexed=False)
    windrichting = db.StringProperty(required=True, indexed=False)
    cijfer = db.FloatProperty(required=True, indexed=False)
    provider = db.StringProperty(required=True)
    #probability_order = db.IntegerProperty(required=True)
