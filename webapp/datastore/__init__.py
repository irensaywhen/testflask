

from sqlalchemy.util import string_types


class BaseDatastore(object):

    def __init__(self, db, model):
        self.db = db
        self.model = model

    def commit(self):
        self.db.session.commit()

    def put(self, model):
        self.db.session.add(model)
        return model

    def put_all(self, models):
        if self._is_listlike(models):
            self.db.session.add_all(models)
            return models

    def delete(self, model):
        self.db.session.delete(model)

    def rollback(self):
        self.db.session.rollback()

    def flush(self):
        self.db.session.flush()

    def get(self, value):
        if isinstance(value, self.model):
            return value
        elif self._is_numeric(value):
            return self.model.query.get(value)
        elif isinstance(value, dict):
            return self.find(**value)
        elif self._is_string_type(value):
            return self.lookup(value)
        else:
            return None

    def lookup(self, value):
        raise NotImplementedError

    def find(self, **value):
        return self.model.query.filter_by(**value).first()

    def remove(self, value, commit=True):
        val = self.get(value)
        self.delete(val)
        if commit:
            self.commit()
        return True

    def create(self, commit=True, **kwargs):
        """Creates and returns a new role from the given parameters."""
        val = self.model(**kwargs)
        self.put(val)
        if commit:
            self.commit()
        return True

    @staticmethod
    def _is_numeric(value):
        try:
            int(value)
        except (TypeError, ValueError):
            return False
        return True

    @staticmethod
    def _is_string_type(value):
        if isinstance(value, string_types):
            return True
        else:
            return False

    @staticmethod
    def _is_listlike(value):
        if isinstance(value, list) or isinstance(value, tuple):
            return True
        else:
            return False



from webapp.datastore.user import RoleDatastore, UserDatastore

class Datastore(object):
    def __init__(self, db, user_model, role_model):
        self.db = db
        self.role = RoleDatastore(db, role_model=role_model)
        self.user = UserDatastore(db, user_model=user_model, role_model=role_model)

