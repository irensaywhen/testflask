from flask import Flask, abort, request

app = Flask(__name__)


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
