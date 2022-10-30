import flask
from flask import request, jsonify

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return '''<h1>Distant Reading Archive</h1>
<p>A prototype API for distant reading of science fiction novels.</p>'''


# A route to return all of the available entries in our catalog.
@app.route('/call', methods=['GET'])
def api_call():
    query_parameters = request.args
    input = query_parameters.get('input')
    return jsonify(model(input))


def model(input):
    return "out" + input


app.run()
