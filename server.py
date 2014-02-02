#! /usr/bin/env python
import jinja2
import random
import socket
import time
import urllib
from urlparse import urlparse, parse_qs

# Global variables
app_content = 'Content-type: application/x-www-form-urlencoded\r\n\r\n' + \
              '<html><body>\r\n'
error_header = 'HTTP/1.0 404 Not Found\r\n'
footer = '</body></html>\r\n'
multi_content = 'Content-type: multipart/form-data\r\n\r\n' + \
                '<html><body>\r\n'
okay_header = 'HTTP/1.0 200 OK\r\n'
text_content = 'Content-type: text/html\r\n\r\n' + \
               '<html><body>\r\n'
loader = jinja2.FileSystemLoader('./templates')
env = jinja2.Environment(loader=loader)


# Methods
def handle_get(conn, path):
    params = parse_qs(urlparse(path)[4])
    page = urlparse(path)[2]

    get_pages = {'/'            : 'index.html',    \
                 '/content'     : 'content.html',  \
                 '/files'       : 'files.html',    \
                 '/images'      : 'images.html',   \
                 '/form'        : 'form_get.html', \
                 '/submit'      : 'submit.html'    }

    if page in get_pages:
        template = env.get_template(get_pages[page])
        conn.send(okay_header)
        conn.send(text_content)
        conn.send(template.render(params))
    else:
        template = env.get_template('error.html')
        conn.send(error_header)
        conn.send(text_content)
        conn.send(template.render())
    conn.send(footer)

def post_request(conn, request):
    return 'HTTP/1.0 200 OK\r\n\r\n' + \
           'This is a post request'

def post_form(conn, params):
    return '<h1>Form Page</h1>\r\n' + \
           '<form action=\'/submit\' method=\'POST\'>\r\n' + \
           'First Name: <input type=\'text\' name=\'firstname\'><br>\r\n' + \
           'Last Name: <input type=\'text\' name=\'lastname\'><br>\r\n' + \
           '<input type=\'submit\' name=\'submit\'>\r\n' + \
           '</form>\r\n'

def post_submit(conn, params):
    return '<h1>Submit Page</h1>\r\n' + \
           'Hello {0} {1}'.format(params['firstname'][0], params['lastname'][0])

def handle_post(conn, request):
    headers = []
    body = ""
    has_body = False

    for line in request.split("\r\n"):
        if has_body:
            body = line
            continue
        if line == "":
            has_body = True
        headers.append(line)

    path = request.split()[1]
    page = urlparse(path)[2]
    params = parse_qs(body)

    post_pages = {'/'       : post_request, \
                  '/form'   : post_form,    \
                  '/submit' : post_submit   }

    conn.send(okay_header)
    conn.send(app_content)
    conn.send(post_pages[page](conn, params))
    conn.send(footer)

def handle_connection(conn):
    request = conn.recv(1000)
    request_type = request.split()[0]
    if request_type == 'GET':
        path = request.split()[1]
        handle_get(conn, path)
    elif request_type == 'POST':
        handle_post(conn, request)
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
