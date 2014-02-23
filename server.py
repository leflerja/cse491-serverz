#!/usr/bin/env python
from app import make_app
import random
import socket
from StringIO import StringIO
from sys import stderr
import time
from urlparse import urlparse
from wsgiref.validate import validator

def handle_connection(conn, port):
    request = conn.recv(1)
    
    if not request:
        print 'Error, remote client closed connection without sending anything'
        return

    count = 0
    env = {}
    while request[-4:] != '\r\n\r\n':
        request += conn.recv(1)

    request, data = request.split('\r\n',1)
    headers = {}
    for line in data.split('\r\n')[:-2]:
        k, v = line.split(': ', 1)
        headers[k.lower()] = v

    path = urlparse(request.split(' ', 3)[1])
    env['REQUEST_METHOD'] = 'GET'
    env['PATH_INFO'] = path[2]
    env['QUERY_STRING'] = path[4]
    env['CONTENT_TYPE'] = 'text/html'
    env['CONTENT_LENGTH'] = str(0)
    env['SCRIPT_NAME'] = ''
    env['SERVER_NAME'] = socket.getfqdn()
    env['SERVER_PORT'] = str(port)
    env['wsgi.version'] = (1, 0)
    env['wsgi.errors'] = stderr
    env['wsgi.multithread']  = False
    env['wsgi.multiprocess'] = False
    env['wsgi.run_once']     = False
    env['wsgi.url_scheme'] = 'http'

    body = ''
    if request.startswith('POST '):
        env['REQUEST_METHOD'] = 'POST'
        env['CONTENT_LENGTH'] = headers['content-length']
        env['CONTENT_TYPE'] = headers['content-type']
        while len(body) < int(headers['content-length']):
            body += conn.recv(1)

    def start_response(status, response_headers):
        conn.send('HTTP/1.0 ')
        conn.send(status)
        conn.send('\r\n')
        for pair in response_headers:
            key, header = pair
            conn.send(key + ': ' + header + '\r\n')
        conn.send('\r\n')

    env['wsgi.input'] = StringIO(body)
    my_app = make_app()
    validator_app = validator(my_app)
    result = my_app(env, start_response)
    for data in result:
        conn.send(data)
    conn.close()

def main(socketmodule=None):
    if socketmodule is None:
        socketmodule = socket

    s = socketmodule.socket()         # Create a socket object
    host = socketmodule.getfqdn()     # Get local machine name
    port = random.randint(8000, 9999)
    s.bind((host, port))              # Bind to the port

    print 'Starting server on', host, port
    print 'The Web server URL for this would be http://%s:%d/' % (host, port)

    s.listen(5)                       # Now wait for client connection

    print 'Entering infinite loop; hit CTRL-C to exit'
    while True:
        # Establish connection with client
        c, (client_host, client_port) = s.accept()
        print 'Got connection from', client_host, client_port
        handle_connection(c, client_port)

if __name__ == '__main__':
    main()
