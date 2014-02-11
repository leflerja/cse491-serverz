import random
import socket
import time
import urlparse

def index(conn):
    conn.send('<h1>Hello, world.</h1>')
    conn.send('<p>This is foo\'s Web server.</p>')
    conn.send('<p><a href = "content">content</p>')
    conn.send('<p><a href = "file">file</p>')
    conn.send('<p><a href = "image">image</p>')
    conn.send('<p><a href = "form">form</p>')

def content(conn):
    conn.send('<h1>You have reached the content page</h1>')

def file(conn):
    conn.send('<h1>You are currently visiting the file page</h1>')

def image(conn):
    conn.send('<h1>You are looking at the image page</h1>')

def form(conn):
    conn.send('<form action="/submit" method="POST">')
    conn.send('<p>Firstname</p><input type="text" name="firstname">')
    conn.send('<p>Lastname</p><input type="text" name="lastname">')
    conn.send('<input type="submit" value="Submit">')
    conn.send('</form>')

def submit(conn, firstname, lastname):
    # What if a female uses it? It shouldn't be Mr.
    conn.send('<h1>Hello Mr. {firstname} '
              '{lastname}.</h1>'.format(firstname = firstname,
                                        lastname = lastname))

def handle_connection(conn):
    # Recieve is misspelled, it should be receive
    recieve = conn.recv(1000)
    recieve = recieve.split('\n')
    con = recieve[-1]
    recieve = recieve[0].split()
    method = recieve[0]
    path = recieve[1]
    parsed_url = urlparse.urlparse(path)
    path = parsed_url.path

    # send a response
    conn.send('HTTP/1.0 200 OK\r\n')
    conn.send('Content-type: text/html\r\n')
    conn.send('\r\n')

    if method == 'GET':
        if path == '/':
            index(conn)
        elif path == '/content':
            content(conn)
        elif path == '/file':
            file(conn)
        elif path == '/image':
            image(conn)
        elif path == '/form':
            form(conn)
        elif path == '/submit':
            parsed_query = urlparse.parse_qs(parsed_url.query)
            submit(conn, parsed_query['firstname'][0],
                    parsed_query['lastname'][0])
    elif method == 'POST':
        if path == '/':
            conn.send('<h1>We recieved a POST request!</h1>')
        elif path == '/submit':
            parsed_query = urlparse.parse_qs(con)
            submit(conn, parsed_query['firstname'][0],
                         parsed_query['lastname'][0])


    conn.close()

def main():
    s = socket.socket()         # Create a socket object
    host = socket.getfqdn() # Get local machine name
    port = random.randint(8000, 9999)
    s.bind((host, port))        # Bind to the port

    print 'Starting server on', host, port
    print 'The Web server URL for this would be http://%s:%d/' % (host, port)

    s.listen(5)                 # Now wait for client connection.
    

    print 'Entering infinite loop; hit CTRL-C to exit'
    while True:
        # Establish connection with client.    
        c, (client_host, client_port) = s.accept()
        print 'Got connection from', client_host, client_port

        handle_connection(c)

if __name__ == '__main__':
   main()
