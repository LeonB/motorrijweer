from functools import wraps
import flask
from motorrijweer import app
import mytime

def template_test(name=None):
	def decorator(f):
		app.jinja_env.tests[name or f.__name__] = f
		return f
	return decorator
app.template_test = template_test

def add_expires_header(minutes=60):
	def decorator(f):
		@wraps(f)
		def decorated_function(*args, **kwargs):
			tme = (mytime.datetime.today()+mytime.timedelta(minutes=minutes)).strftime('%a, %d %b %Y %H:%M:%S') + ' ' + mytime.datetime.today().tzname()

			data = f(*args, **kwargs)
			if isinstance(data, flask.Response):
			    response = data
			else:
			    response = flask.make_response(data)

			response.headers['Expires'] = tme
			response.headers['Cache-Control'] = 'max-age=%s' % minutes
			return response
		return decorated_function
	return decorator
app.add_expires_header = add_expires_header