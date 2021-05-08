from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin

import pandas as pd

app = Flask(__name__)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/', methods=['GET', 'POST'])
@cross_origin()
def index():
    """Add to Data Source for save&test"""
    print(request.headers, request.get_json())
    return 'Python Grafana data source, used for rendering HTML panels and timeseries data.'


@app.route('/query', methods=['GET', 'POST'])
@cross_origin(max_age=600)
def query_metrics():
    req = request.get_json()
    from_timestamp = int(pd.Timestamp(req['range']['from']).timestamp() * 1000)
    to_timestamp = int(pd.Timestamp(req['range']['from']).timestamp() * 1000)
    print('query from %s to %s.' % (from_timestamp, to_timestamp))
    results = []
    for targets in req['targets']:
        target_str = targets.get('target')
        if target_str == "fd":
            data = pd.read_csv("/Users/4paradigm/cjl/2021/guoso_test/fd.csv", header=None)
            data_points = []
            for i in data.index:
                timestamp = int(data.loc[i].values[1])
                if timestamp >= from_timestamp & timestamp <= to_timestamp:
                    data_points.append([int(data.loc[i].values[0]), int(data.loc[i].values[1])])
                elif timestamp > to_timestamp:
                    break
            result = [
                {
                    "target": "fd",
                    "datapoints": data_points
                }
            ]
            results.extend(result)
        else:
            data = pd.read_csv("/Users/4paradigm/cjl/2021/guoso_test/defunct.csv", header=None)
            data_points = []
            for i in data.index:
                timestamp = int(data.loc[i].values[1])
                if timestamp >= from_timestamp & timestamp <= to_timestamp:
                    data_points.append([int(data.loc[i].values[0]), int(data.loc[i].values[1])])
                elif timestamp > to_timestamp:
                    break
            print(data_points)
            result = [
                {
                    "target": "defunct thread",
                    "datapoints": data_points
                }
            ]
            results.extend(result)
    print(results)
    return jsonify(results)


@app.route('/annotations', methods=['GET', 'POST'])
@cross_origin(max_age=600)
def query_annotations():
    """Add annotation at 2015-12-22 03:17:00"""
    req = request.get_json()
    query_from = pd.Timestamp(req['range']['from']).to_pydatetime()
    query_to = pd.Timestamp(req['range']['to']).to_pydatetime()
    print('query from %s to %s.' % (query_from, query_to))
    annotation = req['annotation']
    query = annotation.get('query')
    results = []
    return jsonify(results)


@app.route('/search', methods=['GET', 'POST'])
@cross_origin()
def find_metrics():
    return jsonify(["fd", "defunct thread"])


@app.route('/panels', methods=['GET', 'POST'])
@cross_origin()
def get_panel():
    req = request.args
    query_from = pd.Timestamp(req['range']['from']).to_pydatetime()
    query_to = pd.Timestamp(req['range']['to']).to_pydatetime()
    print('query from %s to %s.' % (query_from, query_to))
    query = req['query']
    print(query)
    return jsonify([])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
