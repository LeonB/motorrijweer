from motorrijweer import app
import weather
import mytime

@app.template_test('instance')
def instance(obj, type_str):
    return obj.__class__.__name__ == type_str

@app.template_test()
def in_past(obj):
    return obj < mytime.date.today()

@app.template_test()
def in_future(obj):
    return obj > mytime.date.today()

@app.template_test()
def in_database(date, *args, **kwargs):
    return weather.Weather.has_datapunten(datum=date, *args, **kwargs)
