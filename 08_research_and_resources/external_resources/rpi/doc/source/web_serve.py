#
# From http://flask.pocoo.org
#
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from flask_test import app

http_server = HTTPServer(WSGIContainer(app))
http_server.listen(5000)  # serving on port 5000
IOLoop.instance().start()