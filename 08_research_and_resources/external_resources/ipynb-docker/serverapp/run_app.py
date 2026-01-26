#
# WSGI Wrapper for the
# IPython Notebook Server App
# based on Docker Containers
#
# run_app.py
#
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from server_app import app

http_server = HTTPServer(WSGIContainer(app))
http_server.listen(8888)  # serving on port 8888
IOLoop.instance().start()
