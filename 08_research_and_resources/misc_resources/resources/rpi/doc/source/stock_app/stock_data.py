#
# Historical Stock Prices
# with the RPi using Python & Flask
#
# stock_data.py
#
# (c) Dr. Yves J. Hilpisch
# The Python Quants
#

import pandas as pd
import pandas.io.data as web
import matplotlib.pyplot as plt
from flask import Flask, request, render_template, redirect, url_for
from forms import SymbolSearch


app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def main():
    form = SymbolSearch(csrf_enabled=False)
    if request.method == 'POST' and form.validate():
        return redirect(url_for('results', symbol=request.form['symbol'],
                            trend1=request.form['trend1'],
                            trend2=request.form['trend2']))
    return render_template('selection.html', form=form)

@app.route("/symbol/<symbol>+<trend1>+<trend2>")
def results(symbol, trend1, trend2):
    data = web.DataReader(symbol, data_source='yahoo')
    data['Trend 1'] = pd.rolling_mean(data['Adj Close'], window=int(trend1))
    data['Trend 2'] = pd.rolling_mean(data['Adj Close'], window=int(trend2))
    data[['Adj Close', 'Trend 1', 'Trend 2']].plot()
    output = 'results.png'
    plt.savefig('static/' + output)
    table = data.tail().to_html()
    return render_template('results.html', symbol=symbol,
                            output=output, table=table)


if __name__ == '__main__':
    app.run(debug=True)