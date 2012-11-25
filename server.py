from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from app import app
import daemon

log = open('tornado.log', 'a+')
ctx = daemon.DaemonContext(stdout=log, stderr=log,
		working_directory='.')
ctx.open() 

http_server = HTTPServer(WSGIContainer(app))
http_server.listen(80)
IOLoop.instance().start()
