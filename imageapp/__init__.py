# __init__.py is the top level file in a Python package.

from quixote.publish import Publisher

# this imports the class RootDirectory from the file 'root.py'
from .root import RootDirectory
from . import html, image

def create_publisher():
     p = Publisher(RootDirectory(), display_exceptions='plain')
     p.is_thread_safe = True
     return p
 
def setup():                            # stuff that should be run once.
    html.init_templates()
    some_data = open('images/dice.png', 'rb').read()
    img = image.add_image_metadata(some_data, "dice.png", "A picture of dice")
    image.add_image(img)

def teardown():                         # stuff that should be run once.
    pass
