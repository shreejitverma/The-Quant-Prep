#!flask/bin/python
import numpy as np
import datetime as dt
from flask import Flask, jsonify


app = Flask(__name__)

tick =  {
            "instrument": "EUR_USD",
            "time": "2014-03-07T20:58:07.461445Z",
            "bid": 1.3500,
            "ask": 1.3501
        }

@app.route('/prices', methods=['GET'])
def get_tasks():
    tick['ask'] = np.round(np.random.normal(1.35, 0.1), 5)
    tick['bid'] = tick['ask'] + 0.0001
    tick['time'] = str(dt.datetime.now()).replace(' ', 'T') + 'Z'
    return jsonify({'tick': tick})

if __name__ == '__main__':
    app.run(debug=True)