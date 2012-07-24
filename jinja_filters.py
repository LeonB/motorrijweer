import flask
from motorrijweer import app
from weather import Beaufort
import mytime

@app.template_filter()
def kmh_to_beaufort(s):
    return Beaufort.from_kmh(s)

@app.template_filter()
def timedelta(date, *args, **kwargs):
    return date + mytime.timedelta(*args, **kwargs)

@app.template_filter()
def datestr(date):
    delta = date - mytime.date.today()
    if delta.days == 0:
        return 'vandaag'
    elif delta.days == 1:
        return 'morgen'
    elif delta.days == 2:
        return 'overmorgen'
    elif delta.days == -1:
        return 'gisteren'
    elif delta.days == -2:
        return 'eergisteren'
    else:
        return None

@app.template_filter()
def is_active(request, pages):
    if isinstance(pages, str):
        pages = [pages]

    endpoint = request.endpoint

    for p in pages:
        if p == endpoint:
            return 'active'

    return ''
