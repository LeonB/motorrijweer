from motorrijweer import app
from weather import Beaufort
import mytime

@app.template_filter()
def kmh_to_beaufort(s):
    return Beaufort.from_kmh(s)

@app.template_filter()
def datestr(s):
    delta = s - mytime.date.today()
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
