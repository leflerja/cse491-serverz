#!/usr/bin/env python
import random
import socket
import time
import webob



class Cse491server(object):

    #initiliaze server then listen for client
    def __init__(self):
        self.sock = socket.socket()         # Create a socket object
        self.host = socket.getfqdn() # Get local machine name
        self.port = random.randint(8000, 9999)
        self.sock.bind((self.host, self.port))        # Bind to the port

        print 'Starting server on', self.host, self.port
        print 'The Web server URL for this would be http://%s:%d/' % (self.host, self.port)

        self.sock.listen(5)                 # Now wait for client connection.

    def wait_for_connect(self):
        # Establish connection with client.    
        self.conn, (client_host, client_port) = sock.accept()
        
        print 'Got connection from', client_host, client_port

    #send response to client
    def send_responses(self):
            cont_type = "Content-Type: text/html"
            response_type = "HTTP/1.1"
            response_status = "200"
            response_status_text = "OK"
            self.response_body = "<html><body><h1>Hello world!</h1></body></html>"
            
            self.conn.send("%s %s %s" % response_type, response_status, response)
            self.conn.send("\n")
            self.conn.send(response_body)

    def close_conn():
        self.conn.send('Thank you for connecting')
        self.conn.send("good bye.")
        self.conn.close()

        
def main():
    server = Cse491server()

    server.wait_for_connect()

    #print 'Entering infinite loop; hit CTRL-C to exit'
    
    while True:
        server.send_responses()
    
    server.close_conn()
    
    
def init_response():
    res = webob.Response()
    res.status_int = 200
    res.headerlist = [('Content-Type', 'text/html')]
    res.body = "<h1>Hello World!</h1>"

    return res

main()
