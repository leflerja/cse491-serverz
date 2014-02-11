import server

# Need to add a test for main()

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

    def close(self):
        self.is_closed = True

# Test a basic GET call.

def test_handle_connection_index():
    conn = FakeConnection("GET / HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n' + \
                      '\r\n' + \
                      '<h1>Hello, world.</h1>' + \
                      '<p>This is foo\'s Web server.</p>' + \
                      '<p><a href = "content">content</p>' + \
                      '<p><a href = "file">file</p>' + \
                      '<p><a href = "image">image</p>' \
                      '<p><a href = "form">form</p>'

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_handle_connection_content():
    conn = FakeConnection("GET /content HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n' + \
                      '\r\n' + \
                      '<h1>You have reached the content page</h1>'

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_handle_connection_file():
    conn = FakeConnection("GET /file HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n' + \
                      '\r\n' + \
                      '<h1>You are currently visiting the file page</h1>'

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_handle_connection_image():
    conn = FakeConnection("GET /image HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n' + \
                      '\r\n' + \
                      '<h1>You are looking at the image page</h1>'

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_handle_connection_post():
    conn = FakeConnection("POST / HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n' + \
                      '\r\n' + \
                      '<h1>We recieved a POST request!</h1>'

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_handle_connection_form():
    conn = FakeConnection("GET /form HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
             'Content-type: text/html\r\n' + \
              '\r\n' + \
    '<form action="/submit" method="GET">' + \
                  '<p>Firstname</p><input type="text" name="firstname">' + \
      '<p>Lastname</p><input type="text" name="lastname">''<input type="submit" value="Submit">' + \
    '</form>'

    server.handle_connection(conn)

def test_handle_connection_submit_get():
    conn = FakeConnection("GET /submit?firstname=X&lastname=Y HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                        'Content-type: text/html\r\n' + \
                         '\r\n' + \
                     '<h1>Hello Mr. X Y</h1>'

    server.handle_connection(conn)

def test_handle_connection_submit_post():
    conn = FakeConnection("POST /submit HTTP/1.0" + \
                          "Content-Type: application/x-www-form-urlencoded" + \
                          "Content-Length: 30\r\n\r\n" + \
                          "firstname=X&lastname=Y")
    expected_return = expected_return = 'HTTP/1.0 200 OK\r\n' + \
                                    'Content-type: text/html\r\n' + \
                                    '\r\n' + \
                                    '<h1>Hello Mr. X Y</h1>'
    server.handle_connection(conn)
