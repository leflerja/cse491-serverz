#! /usr/bin/env python
import server

# Test the 404 Error page
def test_error():
    conn = FakeConnection("GET /error HTTP/1.0\r\n\r\n")
    server.handle_connection(conn)
    result = conn.sent

    if ('HTTP/1.0 404 Not Found' and \
        'Content-type: text/html' and \
        'Error Page' and \
        'This page does not exist') not in result:
        assert False
    else:
        pass

# Test the Index page
def test_index():
    conn = FakeConnection("GET / HTTP/1.0\r\n\r\n")
    server.handle_connection(conn)
    result = conn.sent

    if ('HTTP/1.0 200 OK' and \
        'Content-type: text/html' and \
        'Hello World!') not in result:
        assert False
    else:
        pass

# Test the Content page
def test_content():
    conn = FakeConnection("GET /content HTTP/1.0\r\n\r\n")
    server.handle_connection(conn)
    result = conn.sent

    if ('HTTP/1.0 200 OK' and \
        'Content-type: text/html' and \
        'Content Page') not in result:
        assert False
    else:
        pass

# Test the Files page
def test_files():
    conn = FakeConnection("GET /files HTTP/1.0\r\n\r\n")
    server.handle_connection(conn)
    result = conn.sent

    if ('HTTP/1.0 200 OK' and \
        'Content-type: text/html' and \
        'Files Page') not in result:
        assert False
    else:
        pass

# Test the Images page
def test_images():
    conn = FakeConnection("GET /images HTTP/1.0\r\n\r\n")
    server.handle_connection(conn)
    result = conn.sent

    if ('HTTP/1.0 200 OK' and \
        'Content-type: text/html' and \
        'Images Page') not in result:
        assert False
    else:
        pass

# Test the Form page
def test_form():
    conn = FakeConnection("GET /form HTTP/1.0\r\n\r\n")
    server.handle_connection(conn)
    result = conn.sent

    if ('HTTP/1.0 200 OK' and \
        'Content-type: text/html' and \
        '<form action=\'/submit\' method=\'GET\'>\r\n' and \
        'First Name: <input type=\'text\' name=\'firstname\'><br>\r\n' and \
        'Last Name: <input type=\'text\' name=\'lastname\'><br>\r\n' and \
        '<input type=\'submit\' name=\'submit\'>\r\n' and \
        '</form>') not in result:
        assert False
    else:
        pass

# Test the Submit page
def test_submit():
    conn = FakeConnection("GET /submit?firstname=Jason&lastname=Lefler&submit=Submit HTTP/1.0\r\n\r\n")
    server.handle_connection(conn)
    result = conn.sent

    if ('HTTP/1.0 200 OK' and \
        'Hello Jason Lefler') not in result:
        assert False
    else:
        pass

# Test the Post page
def test_post():
    conn = FakeConnection("POST /form HTTP/1.0\r\n\r\n")
    server.handle_connection(conn)
    result = conn.sent

    if ('HTTP/1.0 200 OK' and \
        'Content-type: application/x-www-form-urlencoded\r\n\r\n') not in result:
        assert False
    else:
        pass

# Test the Post Form page
def test_post_form():
    conn = FakeConnection("POST /form HTTP/1.0\r\n\r\n")
    server.handle_connection(conn)
    result = conn.sent

    if ('HTTP/1.0 200 OK' and \
        'Content-type: application/x-www-form-urlencoded\r\n\r\n' and \
        '<form action=\'/submit\' method=\'POST\'>\r\n' and \
        'First Name: <input type=\'text\' name=\'firstname\'><br>\r\n' and \
        'Last Name: <input type=\'text\' name=\'lastname\'><br>\r\n' and \
        '<input type=\'submit\' name=\'submit\'>\r\n' and \
        '</form>') not in result:
        assert False
    else:
        pass

# Test the Post Submit page
def test_submit():
    conn = FakeConnection("POST /submit HTTP/1.0\r\nHost: mse.edu\r\n\r\nfirstname=Jason&lastname=Lefler")
    server.handle_connection(conn)
    result = conn.sent

    if ('HTTP/1.0 200 OK' and \
        'Hello Jason Lefler') not in result:
        assert False
    else:
        pass

class FakeConnection(object):
    """
    A fake connection class that mimics a real TCP socket for the purpose
    of testing socket I/O.
    """
    def __init__(self, to_recv):
        self.to_recv = to_recv
        self.sent = ""
        self.is_closed = False

    def recv(self, n):
        if n > len(self.to_recv):
            r = self.to_recv
            self.to_recv = ""
            return r
            
        r, self.to_recv = self.to_recv[:n], self.to_recv[n:]
        return r

    def send(self, s):
        self.sent += s

    def settimeout(self, n):
        self.timeout = n

    def close(self):
        self.is_closed = True
