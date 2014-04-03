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

def image_search(name, desc):
    indexes = index_search(name, desc)
    img_results = {'img' : 'img'}
    img_results['results'] = []
    for i in indexes:
        result = {'index' : i}
        result['name'] = images[i]['name']
        result['desc'] = images[i]['desc']
        img_results['results'].append(result)
    return img_results

def index_search(name, desc):
    img_index = []
    cnt = 0
    for item in images:
        if (item['name'] == name) or (desc in item['desc']):
            img_index.append(cnt)
        cnt += 1
    return img_index

def update_list(form_data):
    img_idx = int(form_data['i'])
    latest = len(images) + 1
    images.append(images[img_idx])
    curr = img_idx + 1

    while (curr < latest):
        images[img_idx] = images[curr]
        img_idx += 1
        curr += 1
    junk = images.pop()
