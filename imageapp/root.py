import quixote
from quixote.directory import Directory, export, subdir

from . import html, sqlite

class RootDirectory(Directory):
    _q_exports = []

    @export(name='')
    def index(self):
        posts = sqlite.get_comments()
        return html.render('image.html', posts)

    @export(name='add_comment')
    def add_comment(self):
        request = quixote.get_request()
        user = request.get_cookie('User')
        comment = request.form['comm']

        message = sqlite.check_comment(user, comment)
        posts = sqlite.get_comments()
        posts['message'] = []
        posts['message'].append(dict(alert=message))

        return html.render('image.html', posts)

    @export(name='create_user')
    def create_user(self):
        return html.render('create_user.html')

    @export(name='create_account')
    def create_account(self):
        request = quixote.get_request()

        name = request.form['username']
        password = request.form['password']
        results = sqlite.create_account(name, password)

        return html.render('create_user.html', results)

    @export(name='css')
    def css(self):
        response = quixote.get_response()
        response.set_content_type('text/css')
        return html.load_file('touching.css')

    @export(name='delete_comment')
    def delete_comment(self):
        request = quixote.get_request()
        comm_owner = request.get_cookie('User')

        message = sqlite.delete_comment(request.form, comm_owner)
        posts = sqlite.get_comments()
        posts['message'] = []
        posts['message'].append(dict(alert=message))

        return html.render('image.html', posts)

    @export(name='delete_image')
    def delete_image(self):
        request = quixote.get_request()
        file_owner = request.get_cookie('User')

        message = sqlite.delete_image(request.form, file_owner)
        results = sqlite.get_image_list()
        results['message'] = []
        results['message'].append(dict(alert=message))

        return html.render('image_list.html', results)

    @export(name='delete_user')
    def delete_user(self):
        request = quixote.get_request()
        sqlite.delete_user(request.form)
        results = sqlite.users_list()
        return html.render('users.html', results)

    @export(name='image_list')
    def image_list(self):
        results = sqlite.get_image_list()
        return html.render('image_list.html', results)

    @export(name='image')
    def image(self):
        posts = sqlite.get_comments()
        return html.render('image.html', posts)

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
        request = quixote.get_request()

        name = request.form['username']
        password = request.form['password']
        cookie, results = sqlite.login(name, password)

        if cookie:
            request.response.set_cookie('User', name)
        return html.render('login.html', results)

    @export(name='logout')
    def logout(self):
        quixote.get_response().set_cookie('User', "null")
        return quixote.redirect('./')

    @export(name='search')
    def search(self):
        return html.render('search.html')

    @export(name='search_result')
    def search_result(self):
        request = quixote.get_request()

        file_name = request.form['name']
        file_owner = request.form['owner']
        file_desc = request.form['desc']

        results = sqlite.image_search(file_name, file_owner, file_desc)
        return html.render('search_results.html', results)

    @export(name='thumb')
    def image_thumbnails(self):
        results = sqlite.get_indexes()
        return html.render('thumbnail.html', results)

    @export(name='update_latest')
    def update_latest(self):
        request = quixote.get_request()
        sqlite.update_latest(request.form)
        posts = sqlite.get_comments()
        return html.render('image.html', posts)

    @export(name='upload')
    def upload(self):
        return html.render('upload.html')

    @export(name='upload_receive')
    def upload_receive(self):
        request = quixote.get_request()

        f_data = request.form['file']
        f_name = request.form['name']
        f_owner = request.get_cookie('User')
        f_desc = request.form['desc']

        message = sqlite.upload_image(f_data, f_name, f_owner, f_desc)
        return html.render('upload.html', message)

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
