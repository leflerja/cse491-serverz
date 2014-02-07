import jinja2
import sys

loader = jinja2.FileSystemLoader('./templates')
env = jinja2.Environment(loader=loader)

filename = sys.argv[1]

print >>sys.stderr, '** Rendering:', filename

template = env.get_template(filename)
