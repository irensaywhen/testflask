
from webapp.app import db
from webapp.util import slugify, now



######

post_tags = db.Table(
    'post_tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'))
)


class Post(db.Model):
    """
    Blog Post Model
    """
    __tablename__ = 'post'

    id = db.Column(db.Integer, db.Sequence('seq_%s' % __tablename__.lower()), primary_key=True)
    title = db.Column(db.String(150))
    slug = db.Column(db.String(100), unique=True)
    body = db.Column(db.Text)
    status = db.Column(db.SmallInteger)
    created_timestamp = db.Column(db.DateTime, default=now(), nullable=False)
    modified_timestamp = db.Column(db.DateTime, default=now(), onupdate=now())

    tags = db.relationship('Tag', secondary=post_tags,
                           backref=db.backref('posts', lazy='dynamic'))

    def __init__(self, *args, **kwargs):
        super(Post, self).__init__(*args, **kwargs)  # Call parent constructor.
        self.generate_slug()

    def generate_slug(self):
        self.slug = ''
        if self.title:
            self.slug = slugify(self.title)

    def __repr__(self):
        return '<Post: %s>' % self.title


class Tag(db.Model):
    """
    Tag Model
    """
    __tablename__ = 'tag'

    id = db.Column(db.Integer, db.Sequence('seq_%s' % __tablename__.lower()), primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    slug = db.Column(db.String(64), unique=True, nullable=False)

    def __init__(self, *args, **kwargs):
        super(Tag, self).__init__(*args, **kwargs)
        self.slug = slugify(self.name)

    def __repr__(self):
        return '<Tag %s>' % self.name
