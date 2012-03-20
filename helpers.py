import mytime

def datums(datum_str):
    # Change input to real date object
    if datum_str == 'vandaag':
        datum = mytime.date.today()
    elif datum_str == 'morgen':
        datum = mytime.date.tomorrow()
    elif datum_str == 'overmorgen':
        datum = mytime.date.day_after_tomorrow()
    elif datum_str == 'gisteren':
        datum = mytime.date.yesterday()
    elif datum_str == 'eergisteren':
        datum = mytime.date.day_before_yesterday()
    else:
        datum = mytime.datetime.strptime(datum_str, '%d%m%Y').date()

    return datum

def link_back(datum):
    datum = datum - mytime.timedelta(days=1)
    datum_str = jinja_filters.datestr(datum)
    return (datum_str if datum_str else datum)

def link_forward(datum):
    datum = datum + mytime.timedelta(days=1)
    datum_str = jinja_filters.datestr(datum)
    return (datum_str if datum_str else datum)