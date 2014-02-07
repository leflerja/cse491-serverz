#! /usr/bin/env python
import server

def test_error():
    conn = FakeConnection("GET /error HTTP/1.0\r\n\r\n")
    server.handle_connection(conn)
    result = conn.sent

    if 'HTTP/1.0 404 Not Found' not in result:
        assert False
    else:
        pass

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

def test_submit():
    conn = FakeConnection("GET /submit?firstname=Jason&lastname=Lefler&submit=Submit HTTP/1.0\r\n\r\n")
    server.handle_connection(conn)
    result = conn.sent

    if ('HTTP/1.0 200 OK' and \
        'Hello Jason Lefler') not in result:
        assert False
    else:
        pass

def test_post_app():
    conn = FakeConnection("POST /submit HTTP/1.0\r\n" + \
                          "Content-Length: 31\r\n" + \
                          "Content-Type: application/x-www-form-urlencoded\r\n\r\n" + \
                          "firstname=Jason&lastname=Lefler\r\n")
    server.handle_connection(conn)
    result = conn.sent

    if 'HTTP/1.0 200 OK' not in result:
        assert False
    else:
        pass

# This doesn't work
#def test_post_multi():
#    conn = FakeConnection("POST /submit HTTP/1.0\r\n" + \
#                          "Content-Length: 187\r\n" + \
#                          "Content-Type: multipart/form-data; boundary=b3f2eea10bf64ea89786c327b60a022a\r\n" + \
#                          "Accept-Encoding: gzip, deflate, compress\r\n" + \
#                          "Accept: */*\r\n" + \
#                          "User-Agent: python-requests/0.14.2 CPython/2.7.3 Darwin/12.5.0\r\n\r\n" + \
#                          "--b3f2eea10bf64ea89786c327b60a022a\r\n" + \
#                          "Content-Disposition: form-data; name='firstname'\r\n" + \
#                          "Content-Type: application/octet-stream\r\n\r\n" + \
#                          "Jason\r\n" + \
#                          "--b3f2eea10bf64ea89786c327b60a022a\r\n" + \
#                          "Content-Disposition: form-data; name='lastname'\r\n" + \
#                          "Content-Type: application/octet-stream\r\n\r\n" + \
#                          "Lefler\r\n" + \
#                          "--b3f2eea10bf64ea89786c327b60a022a--\r\n")
#    server.handle_connection(conn)
#    result = conn.sent
#
#    if 'HTTP/1.0 200 OK' not in result:
#        assert False
#    else:
#        pass

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
