#! /usr/bin/env python

import cgi
import jinja2
import traceback
import urllib
from StringIO import StringIO
from urlparse import urlparse, parse_qs
from wsgiref.simple_server import make_server


def render_page(page, params):
    loader = jinja2.FileSystemLoader('./templates')
    env = jinja2.Environment(loader=loader)
    template = env.get_template(page)
#    x = template.render(params)
    x = template.render(params).encode('latin-1', 'replace')
    return str(x)


class MyApp(object):
    def __call__(self, environ, start_response):
        options = {'/'            : self.index,
                   '/content'     : self.content,
                   '/files'       : self.files,
                   '/images'      : self.images,
                   '/form'        : self.form,
                   '/submit'      : self.submit   }

        path = environ['PATH_INFO']
        page = options.get(path)

        if page is None:
            return self.error(environ, start_response)

        return page(environ, start_response)

    def error(self, environ, start_response):
        start_response('404 Not Found', [('Content-type', 'text/html')])
        return render_page('error.html','')

    def index(self, environ, start_response):
        start_response('200 OK', [('Content-type', 'text/html')])
        return render_page('index.html','')

    def content(self, environ, start_response):
        start_response('200 OK', [('Content-type', 'text/html')])
        return render_page('content.html','')

    def files(self, environ, start_response):
        start_response('200 OK', [('Content-type', 'text/html')])
        return render_page('files.html','')

    def images(self, environ, start_response):
        start_response('200 OK', [('Content-type', 'text/html')])
        return render_page('images.html','')

    def form(self, environ, start_response):
        start_response('200 OK', [('Content-type', 'text/html')])
        return render_page('form.html','')

    def submit(self, environ, start_response):
        method = environ['REQUEST_METHOD']
        if method == 'GET':
            return self.handle_get(environ, start_response)
        else:
            return self.handle_post(environ, start_response)

    def handle_get(self, environ, start_response):
        start_response('200 OK', [('Content-type', 'text/html')])
        params = parse_qs(environ['QUERY_STRING'])
        return render_page('submit.html', params)

    def handle_post(self, environ, start_response):
        con_type = environ['CONTENT_TYPE']
        body = ''
        con_length = int(environ.get('CONTENT_LENGTH', 0))

        if con_type == 'application/x-www-form-urlencoded':
            body = parse_qs(environ['wsgi.input'].read(con_length))
            start_response('200 OK', con_type)
            return render_page('submit.html', body)

        else:
#            body = environ['wsgi.input']
            body = parse_qs(environ['wsgi.input'].read(con_length))
            headers = {}
            for k, v in body.iteritems():
#            for line in body:
#                k, v = line.split(':', 1)
                headers[k.lower()] = v
            fs = cgi.FieldStorage(fp=StringIO(body), headers=headers, environ=environ)
            params ={} 
            for key in fs.keys():
                params[key] = fs[key].value
            start_response('200 OK', con_type)
            return render_page('s2.html', params)
#            return render_page('submit.html', params)
#            temp = {}
#            temp['firstname'] = "Jason"
#            temp['lastname'] = "Lefler"
#            return render_page('s2.html', temp)

def make_app():
    return MyApp()
