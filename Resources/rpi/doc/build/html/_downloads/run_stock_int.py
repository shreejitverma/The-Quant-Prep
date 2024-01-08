#
# WSGI Wrapper for the
# Historical Stock Data App (Interactive)
#
# run_stock_int.py
# 
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from stock_interactive import app

http_server = HTTPServer(WSGIContainer(app))
http_server.listen(8888)  # serving on port 8888
IOLoop.instance().start()