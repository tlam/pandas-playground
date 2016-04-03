from flask import Flask, jsonify
from flask import render_template

from fundamentals.data import Sal

app = Flask(__name__)
LOCATIONS = {
    'canada': {'name': 'Canada', 'data': ['calgary', 'canada', 'edmonton', 'montreal', 'toronto', 'vancouver']},
    'chicago': {'name': 'Chicago', 'data': ['chicago']},
    'new-york': {'name': 'New York', 'data': ['new york']},
    'san-francisco': {'name': 'San Francisco', 'data': ['san francisco']},
    'seattle': {'name': 'Seattle', 'data': ['seattle']},
    'toronto': {'name': 'Toronto', 'data': ['toronto']},
}


@app.route('/')
def index():
    context = {
        'locations': sorted(LOCATIONS.items()),
    }
    return render_template('index.html', **context)


@app.route('/locations/<location>')
def locations(location):
    sal = Sal()
    context = {
        'geo_location': sal.location_data(LOCATIONS[location]['data']),
    }
    return jsonify(**context)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5005)
