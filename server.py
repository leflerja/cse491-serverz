#! /usr/bin/env python
import cgi
import jinja2
import random
import socket
from StringIO import StringIO
import time
import urllib
from urlparse import urlparse, parse_qs


def handle_connection(conn):
    okay_response = 'HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n'
    error_response = 'HTTP/1.0 404 Not Found\r\nContent-type: text/html\r\n\r\n'
    loader = jinja2.FileSystemLoader('./templates')
    env = jinja2.Environment(loader=loader)
    
    request = conn.recv(1)
    count = 0
    while request[-4:] != '\r\n\r\n':
        request += conn.recv(1)
    
    request, headers = request.split('\r\n',1)
    d = {}
    for line in headers.split('\r\n')[:-2]:
        k, v = line.split(': ', 1)
        d[k.lower()] = v

    request_type = request.split()[0]
    path = urlparse(request.split(' ', 3)[1])
    page = path[2]

    my_pages = {'/'            : 'index.html',    \
                '/content'     : 'content.html',  \
                '/files'       : 'files.html',    \
                '/images'      : 'images.html',   \
                '/form'        : 'form_get.html', \
                '/submit'      : 'submit.html'    }

    # Check for POST
    body = ''
    if request_type == 'POST':
        while len(body) < int(d['content-length']):
            body += conn.recv(1)
        e = {'REQUEST_METHOD' : 'POST'}
        fs = cgi.FieldStorage(fp=StringIO(body), headers=d, environ=e)
        params = {}
        for key in fs.keys():
            params[key] = fs[key].value
    else:
        params = parse_qs(path[4])
        
    # Create and send response
    if page not in my_pages:
        template = env.get_template('error.html')
        conn.send(error_response)
    else:
        template = env.get_template(my_pages[page])
        okay_response += template.render(params)
        conn.send(okay_response)
    conn.close()

def main():
    s = socket.socket()         # Create a socket object
    host = socket.getfqdn()     # Get local machine name
    port = random.randint(8000, 9999)
    s.bind((host, port))        # Bind to the port

    print 'Starting server on', host, port
    print 'The Web server URL for this would be http://%s:%d/' % (host, port)
    
    s.listen(5)                 # Now wait for client connection

    print 'Entering infinite loop; hit CTRL-C to exit'
    while True:
        # Establish connection with client
        c, (client_host, client_port) = s.accept()
        print 'Got connection from', client_host, client_port
        handle_connection(c)

if __name__ == '__main__':
    main()
