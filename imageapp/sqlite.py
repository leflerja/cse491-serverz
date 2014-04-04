import os
import sqlite3
import sys

IMAGES_DB = './imageapp/images.sqlite'
image_dir = '../images'


# Create the database if it does not already exist
def create_db(): 
    if not os.path.exists(IMAGES_DB):
        db = sqlite3.connect(IMAGES_DB)
        db.execute('CREATE TABLE image_store ' +
                   '(i INTEGER PRIMARY KEY, image BLOB, ' +
                   'name TEXT, desc TEXT, latest INTEGER DEFAULT 0)');
        db.commit()
        db.close()
        init_load()

# Load all images in ../images directory and metadata from ./image_metadata.txt
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

# The "latest" column is a flag that is set to 1 for the latest image
# selected, and set to 0 for all others
def set_latest(index):
    db = sqlite3.connect(IMAGES_DB)
    db.execute('UPDATE image_store SET latest=0')
    db.execute('UPDATE image_store SET latest=1 WHERE i=?', (index,))
    db.commit()
    db.close()

def get_latest_image():
    db = sqlite3.connect(IMAGES_DB)
    db.text_factory = bytes
    c = db.cursor()

    c.execute('SELECT i, image FROM image_store WHERE latest=1 LIMIT 1')
    i, image = c.fetchone()
    return image

def update_latest(form_data):
    img_idx = int(form_data['i'])
    set_latest(img_idx)

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

    return img_results

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

    return img_results

