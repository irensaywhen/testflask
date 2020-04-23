from flask import Blueprint, render_template

from webapp.app import app

blog = Blueprint(
    'blog',
    __name__,
    template_folder='../templates/')




@blog.route('/')
def index():
    return render_template('index.html')
