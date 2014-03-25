import quixote
from quixote.directory import Directory, export, subdir

from . import html, image

class RootDirectory(Directory):
    _q_exports = []

    @export(name='')                    # this makes it public.
    def index(self):
        return html.render('index.html')

    @export(name='upload')
    def upload(self):
        return html.render('upload.html')

    @export(name='upload_receive')
    def upload_receive(self):
        request = quixote.get_request()
        print request.form.keys()

        the_file = request.form['file']
        print dir(the_file)
        print 'received file with name:', the_file.base_filename
        data = the_file.read(int(1e9))

        image.add_image(data)

        return quixote.redirect('./')

    @export(name='image')
    def image(self):
        return html.render('image.html')

    @export(name='image_raw')
    def image_raw(self):
        response = quixote.get_response()
        response.set_content_type('image/png')
        img = image.get_latest_image()
        return img

    @export(name='body.jpg')
    def body_jpg(self):
        data = html.get_image('body.jpg')
        return data

    @export(name='content.jpg')
    def content_jpg(self):
        data = html.get_image('content.jpg')
        return data

    @export(name='footer.gif')
    def footer_gif(self):
        data = html.get_image('footer.gif')
        return data

    @export(name='header.jpg')
    def header_jpg(self):
        data = html.get_image('header.jpg')
        return data

    @export(name='menubottom.jpg')
    def menubottom_jpg(self):
        data = html.get_image('menubottom.jpg')
        return data

    @export(name='menuhover.gif')
    def menuhover_gif(self):
        data = html.get_image('menuhover.gif')
        return data
