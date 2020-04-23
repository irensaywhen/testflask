
from webapp.app import db
from webapp.util import now
from sqlalchemy.ext.hybrid import hybrid_property


######

class Role(db.Model):
    """Role Data Model"""
    __tablename__ = 'role'
    id = db.Column(db.Integer(), db.Sequence('seq_%s' % __tablename__.lower()), primary_key=True)
    name = db.Column(db.String(60), nullable=False, unique=True)
    fullname = db.Column(db.String(80), unique=True)
    description = db.Column(db.Text)

    def __repr__(self):
        rep = '<%r:(Name:%r)>'
        rep_col = self.__class__.__name__, self.name
        return rep % rep_col


class User(db.Model):
    """User Data Model"""
    __tablename__ = 'user'
    id = db.Column(db.Integer(), db.Sequence('seq_%s' % __tablename__.lower()), primary_key=True, index=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    active = db.Column(db.Boolean(), nullable=False, default=True)
    current_login_at = db.Column(db.DateTime, default=now(), nullable=False)
    created_at = db.Column(db.DateTime, default=now(), nullable=False)
    modified_at = db.Column(db.DateTime, onupdate=now())
    login_count = db.Column(db.Integer)

    id_created_by = db.Column(db.Integer, db.ForeignKey('user.id', name='fk_user_created'), index=True)
    id_role = db.Column(
        db.Integer, db.ForeignKey('role.id', name='fk_user_role'), index=True, nullable=False)

    created_by = db.relationship('User',  primaryjoin='User.id==User.id_created_by', lazy='joined')
    role = db.relationship('Role', backref=db.backref("users"))
