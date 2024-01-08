#
# WSGI Wrapper for the
# Historical Stock Data App
#
# run_stock_app.py
#
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from stock_data import app

http_server = HTTPServer(WSGIContainer(app))
http_server.listen(8888)  # serving on port 8888
IOLoop.instance().start()