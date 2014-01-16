#!/usr/bin/env python
import random
import socket
import time


class Cse491server(object):

    # initiliaze server then listen for client
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
        self.conn, (self.client_host, self.client_port) = self.sock.accept()
        
        print 'Got connection from', self.client_host, self.client_port

    # send response to client
    def send_responses(self):
        cont_type = "Content-Type: text/html\n\n"
        response_type = "HTTP/1.0 "
        response_line = "200 OK\n"
        
        response_body = "<html><body><h1>Hello, world!</h1> \
                        <p>This is koppmana's web server!</p> \
                        </body></html>"
        
        self.conn.send(response_type + response_line)
        self.conn.send(cont_type)
        self.conn.send(response_body)
                
    # close socket connection
    def close_conn(self):
        self.conn.close()
        print "Disconnected from " + self.client_host

        
def main():
    server = Cse491server()

    print 'Entering infinite loop; hit CTRL-C to exit'
    while True:
        server.wait_for_connect()
        
    
        server.send_responses()
        
        server.close_conn()
    

main()
