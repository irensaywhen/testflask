import datetime, re


now = datetime.datetime.utcnow


def slugify(s):
    return re.sub('[^\w]+', '-', s).lower()

