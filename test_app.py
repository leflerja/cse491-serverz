#! /usr/bin/env python

import app
import urllib
from StringIO import StringIO


def test_error():
    environ = {}
    environ['PATH_INFO'] = '/error'
    environ['REQUEST_METHOD'] = 'GET'
    environ['QUERY_STRING'] = ''
    environ['CONTENT_TYPE'] = 'text/html'

    d = {}
    def test_start_response(s, h, return_in=d):
        d['status'] = s
        d['headers'] = h

    test_app = app.MyApp()
    results = test_app(environ, test_start_response)

    text = "".join(results)
    status, headers = d['status'], d['headers']
    
    assert text.find('Error') != -1, text
    assert status == '404 Not Found'
    assert ('Content-type', 'text/html') in headers

def test_index():
    environ = {}
    environ['PATH_INFO'] = '/'
    environ['REQUEST_METHOD'] = 'GET'
    environ['QUERY_STRING'] = ''
    environ['CONTENT_TYPE'] = 'text/html'

    d = {}
    def test_start_response(s, h, return_in=d):
        d['status'] = s
        d['headers'] = h

    test_app = app.MyApp()
    results = test_app(environ, test_start_response)

    text = "".join(results)
    status, headers = d['status'], d['headers']
    
    assert text.find('Hello') != -1, text
    assert status == '200 OK'
    assert ('Content-type', 'text/html') in headers

def test_content():
    environ = {}
    environ['PATH_INFO'] = '/content'
    environ['REQUEST_METHOD'] = 'GET'
    environ['QUERY_STRING'] = ''
    environ['CONTENT_TYPE'] = 'text/html'

    d = {}
    def test_start_response(s, h, return_in=d):
        d['status'] = s
        d['headers'] = h

    test_app = app.MyApp()
    results = test_app(environ, test_start_response)

    text = "".join(results)
    status, headers = d['status'], d['headers']
    
    assert text.find('Content') != -1, text
    assert status == '200 OK'
    assert ('Content-type', 'text/html') in headers

def test_files():
    environ = {}
    environ['PATH_INFO'] = '/files'
    environ['REQUEST_METHOD'] = 'GET'
    environ['QUERY_STRING'] = ''
    environ['CONTENT_TYPE'] = 'text/html'

    d = {}
    def test_start_response(s, h, return_in=d):
        d['status'] = s
        d['headers'] = h

    test_app = app.MyApp()
    results = test_app(environ, test_start_response)

    text = "".join(results)
    status, headers = d['status'], d['headers']
    
    assert text.find('Files') != -1, text
    assert status == '200 OK'
    assert ('Content-type', 'text/html') in headers

def test_text():
    environ = {}
    environ['PATH_INFO'] = '/text/test.txt'
    environ['REQUEST_METHOD'] = 'GET'
    environ['QUERY_STRING'] = ''
    environ['CONTENT_TYPE'] = 'text/html'

    d = {}
    def test_start_response(s, h, return_in=d):
        d['status'] = s
        d['headers'] = h

    test_app = app.MyApp()
    results = test_app(environ, test_start_response)

    text = "".join(results)
    status, headers = d['status'], d['headers']
    
    assert text.find('This is a text file') != -1, text
    assert status == '200 OK'
    assert ('Content-type', 'text/plain') in headers

def test_images():
    environ = {}
    environ['PATH_INFO'] = '/images'
    environ['REQUEST_METHOD'] = 'GET'
    environ['QUERY_STRING'] = ''
    environ['CONTENT_TYPE'] = 'text/html'

    d = {}
    def test_start_response(s, h, return_in=d):
        d['status'] = s
        d['headers'] = h

    test_app = app.MyApp()
    results = test_app(environ, test_start_response)

    text = "".join(results)
    status, headers = d['status'], d['headers']
    
    assert text.find('Images') != -1, text
    assert status == '200 OK'
    assert ('Content-type', 'text/html') in headers

def test_images_thumb():
    environ = {}
    environ['PATH_INFO'] = '/images_thumb'
    environ['REQUEST_METHOD'] = 'GET'
    environ['QUERY_STRING'] = ''
    environ['CONTENT_TYPE'] = 'text/html'

    d = {}
    def test_start_response(s, h, return_in=d):
        d['status'] = s
        d['headers'] = h

    test_app = app.MyApp()
    results = test_app(environ, test_start_response)

    text = "".join(results)
    status, headers = d['status'], d['headers']
    
    assert text.find('Images') != -1, text
    assert status == '200 OK'
    assert ('Content-type', 'text/html') in headers

def test_pics():
    environ = {}
    environ['PATH_INFO'] = '/pics/chrome.png'
    environ['REQUEST_METHOD'] = 'GET'
    environ['QUERY_STRING'] = ''
    environ['CONTENT_TYPE'] = 'text/html'

    d = {}
    def test_start_response(s, h, return_in=d):
        d['status'] = s
        d['headers'] = h

    test_app = app.MyApp()
    results = test_app(environ, test_start_response)

    text = "".join(results)
    status, headers = d['status'], d['headers']
    
    assert status == '200 OK'
    assert ('Content-type', 'image/png') in headers

def test_form():
    environ = {}
    environ['PATH_INFO'] = '/form'
    environ['REQUEST_METHOD'] = 'GET'
    environ['QUERY_STRING'] = ''
    environ['CONTENT_TYPE'] = 'text/html'

    d = {}
    def test_start_response(s, h, return_in=d):
        d['status'] = s
        d['headers'] = h

    test_app = app.MyApp()
    results = test_app(environ, test_start_response)

    text = "".join(results)
    status, headers = d['status'], d['headers']
    
    assert text.find('Form') != -1, text
    assert status == '200 OK'
    assert ('Content-type', 'text/html') in headers

def test_submit():
    environ = {}
    environ['PATH_INFO'] = '/submit'
    environ['REQUEST_METHOD'] = 'GET'
    environ['QUERY_STRING'] = 'firstname=Jason&lastname=Lefler&submit=Submit'
    environ['CONTENT_TYPE'] = 'text/html'

    d = {}
    def test_start_response(s, h, return_in=d):
        d['status'] = s
        d['headers'] = h

    test_app = app.MyApp()
    results = test_app(environ, test_start_response)

    text = "".join(results)
    status, headers = d['status'], d['headers']
    
    assert text.find('Submit') != -1, text
    assert text.find('Jason') != -1, text
    assert text.find('Lefler') != -1, text
    assert status == '200 OK'
    assert ('Content-type', 'text/html') in headers

def test_post_app():
    environ = {}
    environ['PATH_INFO'] = '/submit'
    environ['REQUEST_METHOD'] = 'POST'
    environ['QUERY_STRING'] = ''
    environ['CONTENT_LENGTH'] = '31'
    environ['CONTENT_TYPE'] = 'application/x-www-form-urlencoded'
    environ['wsgi.input'] = StringIO("firstname=Jason&lastname=Lefler")

    d = {}
    def test_start_response(s, h, return_in=d):
        d['status'] = s
        d['headers'] = h

    test_app = app.MyApp()
    results = test_app(environ, test_start_response)

    text = "".join(results)
    status, headers = d['status'], d['headers']
    
    assert text.find('Submit') != -1, text
    assert text.find('Jason') != -1, text
    assert text.find('Lefler') != -1, text
    assert status == '200 OK'

def test_post_multi():
    content = "--AaB03x\r\n" + \
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
              "--AaB03x--\r\n"
    environ = {}
    environ['PATH_INFO'] = '/submit'
    environ['REQUEST_METHOD'] = 'POST'
    environ['QUERY_STRING'] = ''
    environ['CONTENT_LENGTH'] = '31'
    environ['CONTENT_TYPE'] = 'multipart/form-data; boundary=AaB03x'
    environ['wsgi.input'] = StringIO(content)

    d = {}
    def test_start_response(s, h, return_in=d):
        d['status'] = s
        d['headers'] = h

    test_app = app.MyApp()
    results = test_app(environ, test_start_response)

    text = "".join(results)
    status, headers = d['status'], d['headers']
    
    assert text.find('Submit') != -1, text
    assert text.find('Jason') != -1, text
    assert text.find('Lefler') != -1, text
    assert status == '200 OK'

