import quixote
from quixote.directory import Directory, export, subdir

from . import html, sqlite

class RootDirectory(Directory):
    _q_exports = []

    @export(name='')
    def index(self):
        return html.render('index.html')

    @export(name='create_user')
    def create_user(self):
        return html.render('create_user.html')

    @export(name='create_account')
    def create_account(self):
        message = 'Your account has been created and you are logged in as '
        request = quixote.get_request()

        name = request.form['username']
        password = request.form['password']
        result = sqlite.create_account(name, password)

        if result == 'error':
            message = 'That username is already taken, please try again'

        return html.render('create_user.html', message)

    @export(name='css')
    def css(self):
        response = quixote.get_response()
        response.set_content_type('text/css')
        return html.load_file('touching.css')

    @export(name='delete_user')
    def delete_user(self):
        request = quixote.get_request()
        sqlite.delete_user(request.form)
        results = sqlite.users_list()
        return html.render('users.html', results)

    @export(name='gallery')
    def image_gallery(self):
        results = sqlite.get_image_gallery()
        return html.render('gallery.html', results)

    @export(name='image')
    def image(self):
        return html.render('image.html')

    @export(name='image_raw')
    def image_raw(self):
        response = quixote.get_response()
        img, type = sqlite.get_latest_image()
        response.set_content_type(type)
        return img

    @export(name='image_thumb')
    def image_thumb(self):
        request = quixote.get_request()
        img = sqlite.get_image_thumb(request.form)
        return img

    @export(name='login')
    def login(self):
        return html.render('login.html')

    @export(name='login_user')
    def login_user(self):
        return html.render('login_result.html', result)

    @export(name='logout')
    def logout(self):
        return quixote.redirect('./')

    @export(name='search')
    def search(self):
        return html.render('search.html')

    @export(name='search_result')
    def search_result(self):
        request = quixote.get_request()

        file_name = request.form['name']
        file_desc = request.form['desc']

        results = sqlite.image_search(file_name, file_desc)
        return html.render('search_results.html', results)

    @export(name='thumb')
    def image_thumbnails(self):
        results = sqlite.get_indexes()
        return html.render('thumbnail.html', results)

    @export(name='update_latest')
    def update_latest(self):
        request = quixote.get_request()
        sqlite.update_latest(request.form)
        return html.render('image.html')

    @export(name='upload')
    def upload(self):
        return html.render('upload.html')

    @export(name='upload_receive')
    def upload_receive(self):
        request = quixote.get_request()

        the_file = request.form['file']
        file_name = request.form['name']
        file_desc = request.form['desc']
        data = the_file.read(int(1e9))

        sqlite.upload_image(data, file_name, file_desc)

        return quixote.redirect('./')

    @export(name='users')
    def users(self):
        results = sqlite.users_list()
        return html.render('users.html', results)

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
