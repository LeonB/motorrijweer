from motorrijweer import app
from weather import Beaufort

@app.template_filter()
def kmh_to_beaufort(s):
    return Beaufort.from_kmh(s)
