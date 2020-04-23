from flask import Flask, abort, request
from flask_sqlalchemy import SQLAlchemy
from .config import Config
from flask_migrate import Migrate


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


from webapp.view.blog import blog
from webapp.model import blog as blog_model
from webapp.model import user as user_model
from webapp.model.user import Role
from webapp.datastore import Datastore
from webapp.model.user import Role, User
from webapp.datastore import Datastore

ds = Datastore(db, role_model=Role)

app.register_blueprint(blog)

if __name__ == '__main__':
    app.run()
