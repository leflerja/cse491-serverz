# image handling API

# This is a list of image dictionaries
images = []

def add_image(data):
    images.append(data)
    return len(images)

def add_image_metadata(data, name, desc):
    img = {'data' : data}
    img['name'] = name
    img['desc'] = desc

    return img

def get_image(num):
    img = images[num]
    return img['data']

def get_latest_image():
    img = images[len(images) - 1]
    return img['data']
