from motorrijweer import app

def template_test(name=None):
    def decorator(f):
        app.jinja_env.tests[name or f.__name__] = f
        return f
    return decorator
app.template_test = template_test
