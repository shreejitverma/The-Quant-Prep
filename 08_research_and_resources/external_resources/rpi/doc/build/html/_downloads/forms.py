#
# Data input form
# forms.py
#

from wtforms import TextField
from wtforms.fields import SubmitField
from wtforms.validators import DataRequired
from flask.ext.wtf import Form

class SymbolSearch(Form):
    symbol = TextField('<b>Symbol</b> (eg AAPL, MSFT)',
                        validators=[DataRequired()])
    trend1 = TextField('<b>Trend 1</b> (eg 20, 42)',
                        validators=[DataRequired()])
    trend2 = TextField('<b>Trend 2</b> (eg 100, 252)',
                        validators=[DataRequired()])
    submit = SubmitField()