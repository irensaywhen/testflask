import os


class Defaults(object):
    DEFAULT_USER_ROLE = 'user'
    STATUS_PUBLIC = 0
    STATUS_DRAFT = 1


class Config(object):
    APPLICATION_DIR = os.path.dirname(os.path.realpath(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///%s/blog.db' % APPLICATION_DIR
    SQLALCHEMY_TRACK_MODIFICATIONS = True
