from flask import current_app
from werkzeug.local import LocalProxy

from webapp.datastore import BaseDatastore

_config = LocalProxy(lambda: current_app.config)


class RoleDatastore(BaseDatastore):
    def __init__(self, db, role_model):
        BaseDatastore.__init__(self, db, role_model)

    def lookup(self, value):
        val = self.model.query.filter(
            (self.model.name == value) | (self.model.fullname == value)).first()
        return val


class UserDatastore(BaseDatastore):
    def __init__(self, db, user_model, role_model):
        self.role = RoleDatastore(db, role_model)
        BaseDatastore.__init__(self, db, user_model)

    def _prepare_create_args(self, **kwargs):
        kwargs.setdefault('active', True)
        role = kwargs.pop('role', _config.get('DEFAULT_USER_ROLE', 'user'))
        kwargs['role'] = self.role.get(role)
        return kwargs

    def lookup(self, value):
        val = self.model.query.filter(
            (self.model.username == value) | (self.model.email == value)).first()
        if val:
            return val

    def create(self, commit=True, **kwargs):
        """Creates and returns a new value from the given parameters."""
        value = self._prepare_create_args(**kwargs)
        row = self.model(**value)
        rv = self.put(row)
        if commit:
            self.commit()
        return rv
