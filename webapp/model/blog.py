import datetime, re
from webapp.app import db


def slugify(s):
    return re.sub('[^\w]+', '-', s).lower()

now = datetime.datetime.now


class Entry(db.Model):
    """
    Blog Post Model
    """
    __tablename__ = 'entry'

    id = db.Column(db.Integer, db.Sequence('seq_%s' % __tablename__.lower()), primary_key=True)
    title = db.Column(db.String(150))
    slug = db.Column(db.String(100), unique=True)
    body = db.Column(db.Text)
    created_timestamp = db.Column(db.DateTime, default=now(), nullable=False)
    modified_timestamp = db.Column(db.DateTime, default=now(), onupdate=now())

    def __init__(self, *args, **kwargs):
        super(Entry, self).__init__(*args, **kwargs)  # Call parent constructor.
        self.generate_slug()

    def generate_slug(self):
        self.slug = ''
        if self.title:
            self.slug = slugify(self.title)

    def __repr__(self):
        return '<Entry: %s>' % self.title
