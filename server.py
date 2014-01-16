#!/usr/bin/env python
import random
import socket
import time
import webob

s = socket.socket()         # Create a socket object
host = socket.getfqdn() # Get local machine name
port = random.randint(8000, 9999)
s.bind((host, port))        # Bind to the port

print 'Starting server on', host, port
print 'The Web server URL for this would be http://%s:%d/' % (host, port)

s.listen(5)                 # Now wait for client connection.

def main():
    print 'Entering infinite loop; hit CTRL-C to exit'
    while True:
        # Establish connection with client.    
        c, (client_host, client_port) = s.accept()
        response = init_response()
        
        print 'Got connection from', client_host, client_port
        c.send(response)
        c.send('Thank you for connecting')
        c.send("good bye.")
        c.close()

def init_response():
    res = webob.Response()
    res.status_int = 200
    res.headerlist = [('Content-Type', 'text/html')]
    res.body = "<h1>Hello World!</h1>"

    return res

main()
