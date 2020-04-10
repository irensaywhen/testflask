import os

class Config(object):
    APPLICATION_DIR = os.path.dirname(os.path.realpath(__file__))
    DATABASE_URI = 'sqlite:///%s/blog.db' % APPLICATION_DIR
