from mimetypes import guess_type
import os
import re
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
                   '(i INTEGER PRIMARY KEY, image BLOB, owner TEXT, ' +
                   'name TEXT, desc TEXT, latest INTEGER DEFAULT 0)')
        db.execute('CREATE TABLE users ' +
                   '(username TEXT PRIMARY KEY, password TEXT)')
        db.execute('CREATE TABLE comments (ci INTEGER PRIMARY KEY, ' +
                   'i INTEGER, username TEXT, comment TEXT)')
        db.commit()
        db.close()
        init_load()

# Load all images in ../images directory, metadata from
# ./image_metadata.txt, comments from ./comments.txt, and my user info
def init_load():
    dirname = os.path.dirname(__file__)
    i_dir = os.path.join(dirname, image_dir)
    i_dir = os.path.abspath(i_dir)
    metadata = dirname + '/' + 'image_metadata.txt'
    comments = dirname + '/' + 'comments.txt'

    # Load all the images
    for file in sorted(os.listdir(i_dir)):
        image_file = i_dir + '/' + file
        r = open(image_file, 'rb').read()
        i = insert_image(r)

    # Add the image metadata
    file = open(metadata, 'r')
    cnt = 1
    for line in file:
        n, o, d = line.split('|')
        update_metadata(cnt, n, o, d)
        cnt +=1
    file.close()

    # Set the last image loaded as the latest
    set_latest(cnt - 1)

    # Add me
    create_account('jason', 'jason')
    create_account('scott', 'scott')

    # Add comments
    file2 = open(comments, 'r')
    for line2 in file2:
        i, u, c = line2.split('|')
        add_comment(i, u, c)
    file2.close()


###############
# Image Stuff #
###############

def delete_image(form_data, file_owner):
    index = int(form_data['i'])
    message = ''
    
    # Check to see if this was the latest image
    done = is_latest(index)

    db = sqlite3.connect(IMAGES_DB)
    c = db.cursor()

    # Check if the user has permission to delete the image
    c.execute('SELECT owner FROM image_store WHERE i=?', (index,))
    row = c.fetchone()

    if not row[0] == file_owner:
        message = 'Only the owner of the image can delete it!'

    # Delete the image and associated comments
    else:
        db.execute('DELETE FROM comments WHERE i=?', (index,))
        db.execute('DELETE FROM image_store WHERE i=?', (index,))
        db.commit()
 
    db.close()
    return message

def get_image_list():
    img_results = {'img' : 'img'}
    img_results['results'] = []

    db = sqlite3.connect(IMAGES_DB)
    c = db.cursor()

    c.execute('SELECT i, name, desc, owner FROM image_store ORDER BY i ASC')
    for row in c:
        result = {'index' : row[0]}
        result['name'] = row[1]
        result['desc'] = row[2]
        result['owner'] = row[3]
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

# Search by image name, owner, description, or any combination
def image_search(name_in, owner_in, desc_in):
    img_results = {'img' : 'img'}
    img_results['results'] = []
    name = name_in.strip()
    owner = owner_in.strip()
    desc = desc_in.strip()
    new_desc = '%' + desc + '%'

    params = ''
    if name: params += 'n'
    if owner: params += 'o'
    if desc: params += 'd'

    # There are 8 options based on the search parameters given
    options = {'nod' : "name = ? AND owner = ? AND desc LIKE ?",
               'no'  : "name = ? AND owner = ?",
               'nd'  : "name = ? AND desc LIKE ?",
               'n'   : "name = ?",
               'od'  : "owner = ? AND desc LIKE ?",
               'o'   : "owner = ?",
               'd'   : "desc LIKE ?"}

    condition = options.get(params, "name = ?")

    # Ugly way to figure out parameters
    if params == 'nod': args = (name, owner, new_desc,)
    elif params == 'no': args = (name, owner,)
    elif params == 'nd': args = (name, new_desc,)
    elif params == 'od': args = (owner, new_desc,)
    elif params == 'o': args = (owner,)
    elif params == 'd': args = (new_desc,)
    else: args = (name,)

    query = "SELECT i, name, owner, desc FROM image_store WHERE {s}" \
            " ORDER BY i ASC".format(s = condition)

    db = sqlite3.connect(IMAGES_DB)
    c = db.cursor()
    c.execute(query, args)

    for row in c:
        result = {'index' : row[0]}
        result['name'] = row[1]
        result['desc'] = row[2]
        result['owner'] = row[3]
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

# This is called when deleting an image from the database
# If it was the latest image, we need to find a new latest image
def is_latest(index):
    db = sqlite3.connect(IMAGES_DB)
    c = db.cursor()
    c.execute('SELECT i FROM image_store WHERE latest=1')
    row = c.fetchone()

    # If this is the latest image, set the image with the largest
    # index to the latest
    if row[0] == index:
        c.execute('SELECT i FROM image_store WHERE latest=0 ' +
                  'ORDER BY i DESC LIMIT 1')
        row2 = c.fetchone()
        set_latest(row2[0])
    db.close()

    return 1

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

def update_metadata(i, file_name, file_owner, file_desc):
    db = sqlite3.connect(IMAGES_DB)
    vars = (file_name, file_owner, file_desc, i)
    db.execute('UPDATE image_store SET name=?, owner=?, desc=? WHERE i=?', vars)
    db.commit()
    db.close()

# Users must be logged in to upload images
def upload_image(f_data, f_name, f_owner, f_desc):
    user_results = {'users' : 'users'}
    user_results['results'] = []

    if not f_data:
        res = {'message' : 'The image file was empty, please try again'}
        user_results['results'].append(res)
        return user_results

    if not f_name:
        res = {'message' : 'The image must have a file name, please try again'}
        user_results['results'].append(res)
        return user_results

    data = f_data.read(int(1e9))
    logged_in = check_for_user(f_owner)

    if logged_in:
        i = insert_image(data)
        update_metadata(i, f_name, f_owner, f_desc)
        set_latest(i)

        res = {'message' : 'The image was uploaded successfully'}
        user_results['results'].append(res)
        return user_results
    else:
        res = {'message' : 'You must log in to upload an image'}
        user_results['results'].append(res)
        return user_results
 

################################
#  User and Comment Functions  #
################################

def add_comment(i, user, comm):
    args = (i, user, comm,)
    query = 'INSERT INTO comments (i, username, comment) VALUES(?, ?, ?)'

    db = sqlite3.connect(IMAGES_DB)
    db.execute(query, args)
    db.commit()
    db.close()

def add_user(name, password):
    db = sqlite3.connect(IMAGES_DB)

    data = (name, password,)
    db.execute('INSERT INTO users (username, password) VALUES (?, ?)', (data))
    db.commit()
    db.close()

def check_comment(user, comment):
    message = ''
    comm = comment.strip()

    # Check if the user is logged in
    logged_in = check_for_user(user)
    if not logged_in:
        message = 'You must be logged in to comment on images'
        return message

    # Check if the comment is empty
    if not comm:
        message = 'The comment field is empty'
        return message

    # The image being commented on is always the latest
    db = sqlite3.connect(IMAGES_DB)
    c = db.cursor()
    c.execute('SELECT i FROM image_store WHERE latest=1')
    row = c.fetchone()
    i = row[0]
    db.close()

    # The user must be logged in with a comment to reach here
    add_comment(i, user, comm)
    return message

# Check if the username is in the database
def check_for_user(name):
    db = sqlite3.connect(IMAGES_DB)
    c = db.cursor()

    c.execute('SELECT EXISTS (SELECT 1 FROM users ' +
              'WHERE username=?)', (name,))
    row = c.fetchone()
    db.close()

    return row[0]

# Verify the correct username/password combination
def check_login(name, password):
    db = sqlite3.connect(IMAGES_DB)
    c = db.cursor()

    c.execute('SELECT EXISTS (SELECT 1 FROM users ' +
              'WHERE username=? ' +
              'AND password=?)', (name, password,))
    row = c.fetchone()
    db.close()

    return row[0]

def create_account(name, password):
    user_results = {'users' : 'users'}
    user_results['results'] = []
    name_in = name.strip()
    password_in = password.strip()

    # Check if username is alphanumeric and not empty
    if not name_in.isalnum():
        res = {'message' : 'Username can only contain letters and/or numbers'}
        user_results['results'].append(res)
        return user_results

    # Check if password is alphanumeric and not empty
    if not password_in.isalnum():
        res = {'message' : 'Password can only contain letters and/or numbers'}
        user_results['results'].append(res)
        return user_results

    # Check if the username is already taken
    user_exists = check_for_user(name_in)

    if user_exists == 1:
        res = {'message' : 'That username already exists, please try again'}
        user_results['results'].append(res)
    else:
        add_user(name_in, password_in)
        res = {'message' : 'The account was successfully created'}
        user_results['results'].append(res)

    return user_results

def delete_comment(form_data, comm_owner):
    index = int(form_data['ci'])
    message = ''

    db = sqlite3.connect(IMAGES_DB)
    c = db.cursor()

    # Check if the user has permission to delete the comment
    c.execute('SELECT username FROM comments WHERE ci=?', (index,))
    row = c.fetchone()

    if not row[0] == comm_owner:
        message = 'Only the owner of the comment can delete it!'

    # Delete the comment
    else:
        db.execute('DELETE FROM comments WHERE ci=?', (index,))
        db.commit()
 
    db.close()
    return message

# Delete user and associated comments
def delete_user(form_data):
    username = form_data['u']
    db = sqlite3.connect(IMAGES_DB)

    db.execute('DELETE FROM comments WHERE username=?', (username,))
    db.execute('DELETE FROM users WHERE username=?', (username,))
    db.commit()
    db.close()

def get_comments():
    comm_results = {'comm' : 'comm'}
    comm_results['comments'] = []

    db = sqlite3.connect(IMAGES_DB)
    c = db.cursor()

    # The image being commented on is always the latest
    c.execute('SELECT i FROM image_store WHERE latest=1')
    row = c.fetchone()
    i = row[0]

    c.execute('SELECT ci, username, comment FROM comments WHERE i=?', (i,))
    for row in c:
        res = {'index' : row[0]}
        res['user'] = row[1]
        res['words'] = row[2]
        comm_results['comments'].append(res)
    db.close()

    return comm_results

def login(name, password):
    user_results = {'users' : 'users'}
    user_results['results'] = []
    name_in = name.strip()
    password_in = password.strip()

    user_exists = check_for_user(name_in)

    # Check if the username exists
    if user_exists == 0:
        res = {'message' : 'That username does not exist, please try again'}
        user_results['results'].append(res)
        return 0, user_results

    # Check if the username/password combination is valid
    login_okay = check_login(name_in, password_in)

    # The username/password combination was invalid
    if login_okay == 0:
        res = {'message' : 'The login attempt failed, please try again'}
        user_results['results'].append(res)
        return 0, user_results

    res = {'message' : 'You are logged in as %s' % name_in}
    user_results['results'].append(res)
    return 1, user_results

# Get a list of all users in the database
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
