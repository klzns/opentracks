# import Jinja2
from jinja2 import Environment, FileSystemLoader

# import Flask
from flask import Flask
app = Flask(__name__)

# Load template file templates/site.html
TEMPLATE_FILE = "templates/index.html"
templateLoader = FileSystemLoader( searchpath="ui/" )
templateEnv = Environment( loader=templateLoader )
template = templateEnv.get_template(TEMPLATE_FILE)

# List for famous movie rendering
templateData = { "a": 123 }


@app.route('/')
def hello_world():
    return template.render(templateData)

if __name__ == '__main__':
    app.run()
