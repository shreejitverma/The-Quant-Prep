#
# Running IPython Notebook
# in Docker Containers
#
# server_app.py
#
# (c) Dr. Yves J. Hilpisch
# The Python Quants GmbH
#
import os
import string
import random
from IPython.lib import passwd
import datetime as dt
from flask import Flask, request, render_template, redirect, url_for
from flask.ext.sqlalchemy import SQLAlchemy
from forms import Registration

charset = string.uppercase + string.lowercase + string.punctuation

app = Flask(__name__)
app.secret_key = '\xb6\xa5hA\x01{\x0f\xd6su\xeb\xd6:4\x13u^O\x15f\xe3\xaf*\xde'


# Configuration of the App

app.config.update(dict(
	SQLALCHEMY_DATABASE_URI='sqlite:///subscriber.db',
	DEBUG=False,))

if app.config['DEBUG'] is True:
    app.config.update(dict(
        SQLALCHEMY_DATABASE_URI='sqlite:///debug.db'))

# Database Class

db = SQLAlchemy(app)

class Subscriber(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.DateTime())
    first_name = db.Column(db.String(80), unique=False)
    last_name = db.Column(db.String(80), unique=False)
    email = db.Column(db.String(120), unique=False)
    port = db.Column(db.Integer, unique=False)

    def __init__(self, first_name, last_name, email, port):
        self.datetime = dt.datetime.now()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.port = port

    def __repr__(self):
        return '<User %r>' % self.last_name

db.create_all()

port = 9000  # initial value

# Pages and Functionality

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route("/", methods=['GET', 'POST'])
def main():
    with open('time_logging.log', 'a') as f:
        f.write(str(dt.datetime.now()) + '\n')
    global port
    port += 1
    error = None
    form = Registration(csrf_enabled=False)
    if request.method == 'POST' and form.validate():
	try:
    	    subscriber = Subscriber(request.form['first_name'],
                                    request.form['last_name'],
                                    request.form['email'],
                                    port)
    	    db.session.add(subscriber)
    	    db.session.commit()
    	    return redirect(url_for('server', first_name=request.form['first_name']))
        except:
            error = 'Error writing to database.'
    return render_template('registration.html', form=form, error=error)

@app.route("/server/<first_name>")
def server(first_name):
    global port
    pw = ''
    for i in range(8):
        pw += random.choice(charset)
    pws = passwd(pw)
    os.system("sudo docker run -d -t -e 'PW=%s' -e 'PORT=%d' -p %d:%d -m 500m jupserver" 
			% (pws, port, port, port))
    return render_template('server.html', first_name=first_name, port=port, pw=pw)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888, debug=True)
