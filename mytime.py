import datetime as orig_datetime
from motorrijweer import app

class UtcTzinfo(orig_datetime.tzinfo):
  def utcoffset(self, dt): return orig_datetime.timedelta(0)
  def dst(self, dt): return orig_datetime.timedelta(0)
  def tzname(self, dt): return 'UTC'
  def olsen_name(self): return 'UTC'

class timedelta(orig_datetime.timedelta):
    pass

class datetime(object):
    def __new__(self, *args, **kwargs):
        return orig_datetime.datetime(*args, **kwargs)

    @classmethod
    def today(cls):
        return orig_datetime.datetime.now(app.timezone)

    @classmethod
    def from_utc(cls, dt):
        utc = UtcTzinfo()
        # return dt.replace(tzinfo=pytz.timezone('UTC')).astimezone(app.timezone)
        return dt.replace(tzinfo=utc).astimezone(app.timezone)

    @classmethod
    def fromtimestamp(cls, timestamp, tz = None):
        if not tz:
            tz = app.timezone
        return orig_datetime.datetime.fromtimestamp(timestamp, tz)

    @classmethod
    def now(cls, tz=None):
        if not tz:
            tz = app.timezone

        return orig_datetime.datetime.now(tz)

    @classmethod
    def strptime(cls, *args, **kwargs):
        return orig_datetime.datetime.strptime(*args, **kwargs)

    @classmethod
    def combine(cls, *args, **kwargs):
        return orig_datetime.datetime.combine(*args, **kwargs)

class date(object):
    @classmethod
    def today(cls):
        return datetime.now(app.timezone).date()

    @classmethod
    def tomorrow(cls):
        return cls.today() + orig_datetime.timedelta(days=1)

    @classmethod
    def day_after_tomorrow(cls):
        return cls.today() + orig_datetime.timedelta(days=2)

    @classmethod
    def yesterday(cls):
        return cls.today() + orig_datetime.timedelta(days=-1)

    @classmethod
    def day_before_yesterday(cls):
        return orig_datetime.date.today() + orig_datetime.timedelta(days=-2)

    #def plus_day(self):
        #return self + orig_datetime.timedelta(days=+1)

    #def min_day(self):
        #return self + orig_datetime.timedelta(days=-1)


class time(orig_datetime.time):
    pass



#time.oldtime = time.time
#def new_time():
    #return time.oldtime() + offset.seconds
#time.time = new_time

#datetime.old_datetime = datetime.datetime
#class new_datetime(datetime.old_datetime):
    #@classmethod
    #def today(cls):
        #today = datetime.old_datetime.today()
        #return new_datetime(today.year, today.month, today.day, today.hour,
                            #today.minute, today.second)

    #def strftime(self, *args, **kwargs):
        #str = datetime.old_datetime.strftime(self, *args, **kwargs)

        #str = str.replace('January', 'januari') 
        #str = str.replace('February', 'februari') 
        #str = str.replace('March', 'maart') 
        #str = str.replace('April', 'april') 
        #str = str.replace('May', 'mei') 
        #str = str.replace('June', 'juni') 
        #str = str.replace('July', 'juli') 
        #str = str.replace('August', 'augustus') 
        #str = str.replace('September', 'september') 
        #str = str.replace('October', 'oktober') 
        #str = str.replace('November', 'november') 
        #str = str.replace('December', 'december') 
        
        #str = str.replace('Monday', 'maandag') 
        #str = str.replace('Tuesday', 'dinsdag') 
        #str = str.replace('Wednesday', 'woensdag') 
        #str = str.replace('Thursday', 'donderdag') 
        #str = str.replace('Friday', 'vrijdag') 
        #str = str.replace('Saturday', 'zaterdag') 
        #str = str.replace('Sunday', 'Zondag') 

        #return str
    
    #@classmethod
    #def fromtimestamp(self, timestamp, tz = None):
        #if not tz:
            #tz = timezone
        #dt = datetime.old_datetime.fromtimestamp(timestamp, tz)
        #return dt
        #return new_datetime(dt.year, dt.month, dt.day, dt.hour, dt.minute,
                            #dt.second)

##datetime.datetime = new_datetime

