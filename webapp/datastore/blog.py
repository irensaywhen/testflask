from flask import current_app
from werkzeug.local import LocalProxy

from webapp.datastore import BaseDatastore

_config = LocalProxy(lambda: current_app.config)


class PostDatastore(BaseDatastore):
    """
    Abstracted post datastore.
    :param db: The Abstracted SQLAlchemy Instance
    :param post_model: A Post Post model class definition
    :param tag_model: A Post Tag model class definition
    """
    def __init__(self, db, post_model, tag_model):
        self.tag = TagDatastore(db, tag_model, post_model)
        BaseDatastore.__init__(self, db, post_model)

    def _prepare_modify_args(self, post, tags):
        if not self._is_listlike(tags):
            tags = [tags]
        tgs = [self.tag.get(tag) for tag in tags]
        post = self.get(post)
        return post, tgs

    def _prepare_create_args(self, **kwargs):
        status = kwargs.get('status', _config.get('STATUS_PUBLIC'))
        kwargs['status'] = status
        tags = kwargs.get('tags', [])
        for tag in tags:
            rn = tag.name if isinstance(tag, self.tag.model) else tag
            # see if the tags exists
            tags.append(self.tag.get(rn))
        kwargs['tags'] = tags
        return kwargs

    def lookup(self, value):
        val = self.model.query.filter(
            (self.model.title == value) | (self.model.slug == value)).first()
        return val

    def create(self, commit=True, **kwargs):
        """
        Creates and returns a new Post from the given parameters.
        """

        value = self._prepare_create_args(**kwargs)
        row = self.model(**value)
        rv = self.put(row)
        if commit:
            self.commit()
        return rv

    def add_tags(self, post, tags):
        post, tags = self._prepare_modify_args(self, post, tags)
        for tag in tags:
            if tag not in post.tags:
                post.tags.append(tag)


class TagDatastore(BaseDatastore):
    """
    Abstracted post datastore.
    :param db: The Abstracted SQLAlchemy Instance
    :param tag_model: A Post Tag model class definition
    :param post_model: A Post model class definition
    """
    def __init__(self, db, tag_model, post_model):
        self.post = PostDatastore(db, post_model, tag_model)
        BaseDatastore.__init__(self, db, tag_model)

    def _prepare_modify_args(self, tag, post):
        tag = self.get(tag)
        post = self.post.get(post)
        return tag, post

    def _prepare_create_args(self, **kwargs):
        posts = kwargs.get('posts', [])
        for post in posts:
            rn = post.name if isinstance(post, self.post.model) else post
            # see if the posts exists
            posts.append(self.post.get(rn))
        kwargs['posts'] = posts
        return kwargs

    def lookup(self, value):
        val = self.model.query.filter(
            (self.model.name == value) | (self.model.slug == value)).first()
        return val

    def create(self, commit=True, **kwargs):
        """
        Creates and returns a new Tag from the given parameters.
        """

        value = self._prepare_create_args(**kwargs)
        row = self.model(**value)
        rv = self.put(row)
        if commit:
            self.commit()
        return rv