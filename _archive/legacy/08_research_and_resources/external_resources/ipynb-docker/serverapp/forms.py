#
# Data Input Form
# forms.py
#
# (c) Dr. Yves J. Hilpisch
# The Python Quants GmbH
#

from wtforms import TextField
from wtforms.fields import SubmitField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired
from flask.ext.wtf import Form

class Registration(Form):
    first_name = TextField('<b>First Name</b>',
                        validators=[DataRequired()])
    last_name = TextField('<b>Last Name</b>',
                        validators=[DataRequired()])
    email = EmailField('<b>Email Address</b>',
                        validators=[DataRequired()])
    submit = SubmitField()
