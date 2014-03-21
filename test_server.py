#! /usr/bin/env python
import server
import sys

def test_error():
    conn = FakeConnection("GET /error HTTP/1.0\r\n\r\n")
    server.handle_connection(conn, 80)
    result = conn.sent

    if 'HTTP/1.0 404 Not Found' not in result:
        assert False
    else:
        pass

def test_index():
    conn = FakeConnection("GET / HTTP/1.0\r\n\r\n")
    server.handle_connection(conn, 80)
    result = conn.sent

    if ('HTTP/1.0 200 OK' and \
        'Content-type: text/html' and \
        'Hello World!') not in result:
        assert False
    else:
        pass

def test_content():
    conn = FakeConnection("GET /content HTTP/1.0\r\n\r\n")
    server.handle_connection(conn, 80)
    result = conn.sent

    if ('HTTP/1.0 200 OK' and \
        'Content-type: text/html' and \
        'Content Page') not in result:
        assert False
    else:
        pass

def test_files():
    conn = FakeConnection("GET /files HTTP/1.0\r\n\r\n")
    server.handle_connection(conn, 80)
    result = conn.sent

    if ('HTTP/1.0 200 OK' and \
        'Content-type: text/html' and \
        'Files Page') not in result:
        assert False
    else:
        pass

def test_images():
    conn = FakeConnection("GET /images HTTP/1.0\r\n\r\n")
    server.handle_connection(conn, 80)
    result = conn.sent

    if ('HTTP/1.0 200 OK' and \
        'Content-type: text/html' and \
        'Images Page') not in result:
        assert False
    else:
        pass

def test_images_thumb():
    conn = FakeConnection("GET /images_thumb HTTP/1.0\r\n\r\n")
    server.handle_connection(conn, 80)
    result = conn.sent

    if ('HTTP/1.0 200 OK' and \
        'Content-type: text/html' and \
        'Thumbnail Images Page') not in result:
        assert False
    else:
        pass

def test_form():
    conn = FakeConnection("GET /form HTTP/1.0\r\n\r\n")
    server.handle_connection(conn, 80)
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
    server.handle_connection(conn, 80)
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
    server.handle_connection(conn, 80)
    result = conn.sent

    if 'HTTP/1.0 200 OK' not in result:
        assert False
    else:
        pass

def test_post_multi():
    conn = FakeConnection("POST /submit HTTP/1.0\r\n" + \
                          "Content-Length: 187\r\n" + \
                          "Content-Type: multipart/form-data; boundary=AaB03x\r\n\r\n" + \
                          "--AaB03x\r\n" + \
                          "Content-Disposition: form-data; name=\"firstname\";" + \
                          " filename=\"firstname\"\r\n\r\n" + \
                          "Jason\r\n" + \
                          "--AaB03x\r\n" + \
                          "Content-Disposition: form-data; name=\"lastname\";" + \
                          " filename=\"lastname\"\r\n\r\n" + \
                          "Lefler\r\n" + \
                          "--AaB03x\r\n" + \
                          "Content-Disposition: form-data; name=\"key\";" + \
                          " filename=\"key\"\r\n\r\n" + \
                          "value\r\n" + \
                          "--AaB03x--\r\n")
    server.handle_connection(conn, 80)
    result = conn.sent

    if 'HTTP/1.0 200 OK' not in result:
        assert False
    else:
        pass

def test_main():
    fakemodule = FakeSocketModule()
    sys.argv[1] = '-A'
    sys.argv.append('myapp')

    success = False
    try:
        server.main(fakemodule)
    except AcceptCalledMultipleTimes:
        success = True
        pass

    assert success, "Something went wrong"

class AcceptCalledMultipleTimes(Exception):
    pass

class FakeSocketModule(object):
    def getfqdn(self):
        return "fakehost"

    def socket(self):
        return FakeConnection("")

class FakeConnection(object):
    def __init__(self, to_recv):
        self.to_recv = to_recv
        self.sent = ""
        self.is_closed = False
        self.n_times_accept_called = 0

    def accept(self):
        if self.n_times_accept_called > 1:
            raise AcceptCalledMultipleTimes("stop calling accept, please")
        self.n_times_accept_called += 1
        
        c = FakeConnection("")
        return c, ("noclient", 32351)

    def bind(self, param):
        (host, port) = param

    def close(self):
        self.is_closed = True

    def listen(self, n):
        assert n == 5
        if n != 5:
            raise Exception("n should be five you dumby")

    def recv(self, n):
        if n > len(self.to_recv):
            r = self.to_recv
            self.to_recv = ""
            return r
            
        r, self.to_recv = self.to_recv[:n], self.to_recv[n:]
        return r

    def send(self, s):
        self.sent += s
