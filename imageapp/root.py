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
        file_name = request.form['name']
        file_desc = request.form['desc']
        data = the_file.read(int(1e9))

        img = image.add_image_metadata(data, file_name, file_desc)
        image.add_image(img)

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

    @export(name='search')
    def search(self):
        return html.render('search.html')

    @export(name='search_result')
    def search_result(self):
        request = quixote.get_request()

        file_name = request.form['name']
        file_desc = request.form['desc']

        results = image.image_search(file_name, file_desc)
        return html.render('search_results.html', results)

    @export(name='update_latest')
    def update_latest(self):
        request = quixote.get_request()
        image.update_list(request.form)
        return html.render('image.html')

# The below functions are needed for the CSS background images

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
