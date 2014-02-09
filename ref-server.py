#! /usr/bin/env python
import socket
import random
from wsgiref.simple_server import make_server
from app import make_app


the_wsgi_app = make_app()

host = socket.getfqdn()
port = random.randint(8000, 9999)
httpd = make_server('', port, the_wsgi_app)
print "\nServing at http://%s:%d/\n" % (host, port,)
httpd.serve_forever()
