import sys, os
from google.appengine.ext.appstats import recording

# package_dir = "gae-env"
# package_dir = "gae-env/lib/python2.7/site-packages"
package_dir = 'libs'
package_dir_path = os.path.join(os.path.dirname(__file__), package_dir)

# Allow unzipped packages to be imported
# from packages folder
sys.path.insert(0, package_dir_path)

# Append zip archives to path for zipimport
for filename in os.listdir(package_dir_path):
    if filename.endswith((".zip", ".egg", ".tar.gz")):
        sys.path.insert(0, "%s/%s" % (package_dir_path, filename))

from motorrijweer import app

# Check for Google appengine signature
if os.environ['SERVER_SOFTWARE'].startswith('Development'):
    from werkzeug_debugger_appengine import get_debugged_app
    app = get_debugged_app(app)

app = recording.appstats_wsgi_middleware(app)