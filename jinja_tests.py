from motorrijweer import app


@app.template_test('instance')
def instance(obj, type_str):
    return obj.__class__.__name__ == type_str
