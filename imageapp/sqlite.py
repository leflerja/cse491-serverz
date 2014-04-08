from mimetypes import guess_type
import os
import sqlite3
import sys

IMAGES_DB = './imageapp/images.sqlite'
image_dir = '../images'


# DB Creation and Initialization Functions

# Create the database if it does not already exist
# Create the image_store and users tables
def create_db(): 
    if not os.path.exists(IMAGES_DB):
        db = sqlite3.connect(IMAGES_DB)
        db.execute('CREATE TABLE image_store ' +
                   '(i INTEGER PRIMARY KEY, image BLOB, ' +
                   'name TEXT, desc TEXT, latest INTEGER DEFAULT 0)');
        db.execute('CREATE TABLE users ' +
                   '(username TEXT PRIMARY KEY, password TEXT)');
        db.commit()
        db.close()
        init_load()

# Load all images in ../images directory, metadata from
# ./image_metadata.txt, and my user info
def init_load():
    dirname = os.path.dirname(__file__)
    i_dir = os.path.join(dirname, image_dir)
    i_dir = os.path.abspath(i_dir)
    metadata = dirname + '/' + 'image_metadata.txt'

    # Load all the images
    for file in sorted(os.listdir(i_dir)):
        image_file = i_dir + '/' + file
        r = open(image_file, 'rb').read()
        i = insert_image(r)

    # Add the image metadata
    file = open(metadata, 'r')
    cnt = 1
    for line in file:
        n, d = line.split('|')
        update_metadata(cnt, n, d)
        cnt +=1

    # Set the last image loaded as the latest
    set_latest(cnt - 1)

    # Add me
    create_account('jason', 'jason')
    create_account('scott', 'scott')

def get_image_gallery():
    img_results = {'img' : 'img'}
    img_results['results'] = []

    db = sqlite3.connect(IMAGES_DB)
    c = db.cursor()

    c.execute('SELECT i, name, desc FROM image_store ORDER BY i ASC')
    for row in c:
        result = {'index' : row[0]}
        result['name'] = row[1]
        result['desc'] = row[2]
        img_results['results'].append(result)
    db.close()

    return img_results

def get_image_thumb(form_data):
    img_idx = int(form_data['i'])
    db = sqlite3.connect(IMAGES_DB)
    db.text_factory = bytes
    c = db.cursor()

    c.execute('SELECT image FROM image_store WHERE i=?', (img_idx,))
    image = c.fetchone()
    db.close()

    return image[0]

def get_indexes():
    img_results = {'img' : 'img'}
    img_results['results'] = []

    db = sqlite3.connect(IMAGES_DB)
    c = db.cursor()

    c.execute('SELECT i FROM image_store ORDER BY i ASC')
    for row in c:
        result = {'index' : row[0]}
        img_results['results'].append(result)
    db.close()
    
    return img_results    

def get_latest_image():
    db = sqlite3.connect(IMAGES_DB)
    db.text_factory = bytes
    c = db.cursor()

    c.execute('SELECT image, name FROM image_store WHERE latest=1 LIMIT 1')
    image, name = c.fetchone()
    db.close()

    return image, guess_type(name)[0]

def image_search(name, desc):
    img_results = {'img' : 'img'}
    img_results['results'] = []

    db = sqlite3.connect(IMAGES_DB)
    c = db.cursor()

    if desc in ('', ' '):
        c.execute('SELECT i, name, desc FROM image_store ' +
                  'WHERE name = ? ORDER BY i ASC', (name,))
    else:
        new_desc = '%' + desc + '%'
        vars = (name, new_desc,)
        c.execute('SELECT i, name, desc FROM image_store ' +
                  'WHERE name = ? ' + 
                  'OR desc LIKE ? ' + 
                  'ORDER BY i ASC', vars)

    for row in c:
        result = {'index' : row[0]}
        result['name'] = row[1]
        result['desc'] = row[2]
        img_results['results'].append(result)
    db.close()

    return img_results

def insert_image(data):
    db = sqlite3.connect(IMAGES_DB)
    db.text_factory = bytes
    db.execute('INSERT INTO image_store (image) VALUES (?)', (data,))

    c = db.cursor()
    c.execute('SELECT i FROM image_store ORDER BY i DESC LIMIT 1')
    row = c.fetchone()

    db.commit()
    db.close()

    return row[0]

# The "latest" column is a flag that is set to 1 for the latest image
# selected, and set to 0 for all others
def set_latest(index):
    db = sqlite3.connect(IMAGES_DB)
    db.execute('UPDATE image_store SET latest=0')
    db.execute('UPDATE image_store SET latest=1 WHERE i=?', (index,))
    db.commit()
    db.close()

def update_latest(form_data):
    img_idx = int(form_data['i'])
    set_latest(img_idx)

def update_metadata(i, file_name, file_desc):
    db = sqlite3.connect(IMAGES_DB)
    vars = (file_name, file_desc, i)
    db.execute('UPDATE image_store SET name=?, desc=? WHERE i=?', vars)
    db.commit()
    db.close()

def upload_image(data, file_name, file_desc):
    i = insert_image(data)
    update_metadata(i, file_name, file_desc)
    set_latest(i)

# User Functions

def add_user(name, password):
    db = sqlite3.connect(IMAGES_DB)

    data = (name, password,)
    db.execute('INSERT INTO users (username, password) VALUES (?, ?)', (data))
    db.commit()
    db.close()

def check_for_user(name):
    db = sqlite3.connect(IMAGES_DB)
    c = db.cursor()

    c.execute('SELECT EXISTS (SELECT 1 FROM users ' +
              'WHERE username=?)', (name,))
    row = c.fetchone()
    db.close()

    return row[0]

def create_account(name, password):
    user_exists = check_for_user(name)

    if user_exists:
        return 'error'
    else:
        add_user(name, password)
        return 'success'

def delete_user(form_data):
    username = form_data['u']
    db = sqlite3.connect(IMAGES_DB)

    db.execute('DELETE FROM users WHERE username=?', (username,))
    db.commit()
    db.close()

def users_list():
    user_results = {'users' : 'users'}
    user_results['results'] = []

    db = sqlite3.connect(IMAGES_DB)
    c = db.cursor()
    c.execute('SELECT username, password FROM users')

    for row in c:
        result = {'username' : row[0]}
        result['password'] = row[1]
        user_results['results'].append(result)
    db.close()

    return user_results

