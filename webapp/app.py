from flask import Flask, abort, request
from flask_sqlalchemy import SQLAlchemy
from webapp.config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

from webapp.model import blog

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/index')
def index():
    return 'Hello, Flask!'

@app.route('/hello/<name>')
@app.route('/hello/')
def hello(name=None):
    if name is None:
        abort(404)

    return 'Hello, %s' % name


if __name__ == '__main__':
    app.run()
