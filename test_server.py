import server

# These are the global test variables
header = 'HTTP/1.0 200 OK\r\n' + \
         'Content-type: text/html\r\n\r\n' + \
         '<html><body>\r\n'
footer = '</body></html>\r\n'

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

# Test a GET call for the root
def test_get_root():
    conn = FakeConnection("GET / HTTP/1.0\r\n\r\n")
    root_return = '<h1>Hello World!</h1>\r\n' + \
                  "This is leflerja's Web server<br>\r\n" + \
                  "<a href='/content'>Content</a><br>\r\n" + \
                  "<a href='/files'>Files</a><br>\r\n" + \
                  "<a href='/images'>Images</a><br>\r\n" + \
                  "<a href='/form'>Form</a>\r\n"
    expected_return = header + root_return + footer

    server.handle_connection(conn)
    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

# Test a GET call for the content page
def test_get_content():
    conn = FakeConnection("GET /content HTTP/1.0\r\n\r\n")
    content_return = '<h1>Content Page</h1>\r\n' + \
                     'This is the content page\r\n'
    expected_return = header + content_return + footer

    server.handle_connection(conn)
    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

# Test a GET call for the file page
def test_get_file():
    conn = FakeConnection("GET /files HTTP/1.0\r\n\r\n")
    file_return = '<h1>Files Page</h1>\r\n' + \
                  'This is the files page\r\n'
    expected_return = header + file_return + footer

    server.handle_connection(conn)
    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

# Test a GET call for the images page
def test_get_images():
    conn = FakeConnection("GET /images HTTP/1.0\r\n\r\n")
    images_return = '<h1>Images Page</h1>\r\n' + \
                    'This is the images page\r\n'
    expected_return = header + images_return + footer

    server.handle_connection(conn)
    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

# Test a GET call for the form page
def test_get_form():
    conn = FakeConnection("GET /form HTTP/1.0\r\n\r\n")
    form_return = '<h1>Form Page</h1>\r\n' + \
                  '<form action=\'/submit\' method=\'GET\'>\r\n' + \
                  'First Name: <input type=\'text\' name=\'firstname\'><br>\r\n' + \
                  'Last Name: <input type=\'text\' name=\'lastname\'><br>\r\n' + \
                  '<input type=\'submit\' name=\'submit\'>\r\n' + \
                  '</form>\r\n'
    expected_return = header + form_return + footer

    server.handle_connection(conn)
    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

# Test a GET call for the submit page
def test_get_submit():
    conn = FakeConnection("GET /submit?firstname=Jason&lastname=Lefler&submit=Submit HTTP/1.0\r\n\r\n")
    submit_return = '<h1>Submit Page</h1>\r\n' + \
                    'Hello Jason Lefler'
    expected_return = header + submit_return + footer

    server.handle_connection(conn)
    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)
     

# Test a POST call
def test_post():
    conn = FakeConnection("POST / HTTP/1.1\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n\r\n' + \
                      'This is a post request'
