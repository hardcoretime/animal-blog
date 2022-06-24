from .database import db
from flask_login import UserMixin


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    posts = db.relationship('Post', backref='author')

    def __str__(self):
        return f'{self.__class__.__name__}(name={self.name!r})'

    def __repr__(self):
        return str(self)
