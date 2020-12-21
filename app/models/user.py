from flask_login import UserMixin
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask import url_for
import base64
from datetime import datetime, timedelta
import os
from .rectangle import Rectangle
from .triangle import Triangle
from .diamond import Diamond


class User(UserMixin, db.Model):
    """
    Create a User table
    """

    # Ensures table will be named in plural and not in singular
    # as is the name of the model
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(60), index=True,
                          unique=True, nullable=False)
    email = db.Column(db.String(60), index=True, unique=True)
    first_name = db.Column(db.String(60), index=True)
    last_name = db.Column(db.String(60), index=True)
    password_hash = db.Column(db.String(128), nullable=False)
    token = db.Column(db.String(32), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)
    rectangles = db.relationship(
        'Rectangle', cascade='all,delete', backref='users')
    triangle = db.relationship(
        'Triangle', cascade='all,delete', backref='users')
    diamond = db.relationship(
        'Diamond', cascade='all,delete', backref='users')

    def __repr__(self):
        return '<User: {}>'.format(self.username)

    def __init__(self, user_name, password, first_name=None, last_name=None, email=None, token=None, token_expiration=None):
        self.user_name = user_name
        self.password_hash = generate_password_hash(password)
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.token = token
        self.token_expiration = token_expiration

    def set_password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return (self.user_id)

    def to_dict(self):
        data = {
            'user_id': self.user_id,
            'user_name': self.user_name,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            '_links': {
                'self_by_user_name': url_for('api.get_user_by_user_name', user_name=self.user_name),
                'self_by_id': url_for('api.get_user_by_user_id', user_id=self.user_id),
                'update_self_by_user_name': url_for('api.update_user_by_user_name', user_name=self.user_name),
                'update_self_by_user_id': url_for('api.update_user_by_user_id', user_id=self.user_id),
                'create_rectangle': url_for('api.create_rectangle'),
                'create_triangle': url_for('api.create_triangle'),
                'create_square': url_for('api.create_square'),
                'create_diamond': url_for('api.create_diamond')
            }
        }
        return data

    def from_dict(self, data, new_user=False):
        for field in ['user_name', 'email', 'first_name', 'last_name']:
            if field in data and data[field]:
                setattr(self, field, data[field])
        if new_user and 'password' in data:
            self.set_password(data['password'])

    def get_token(self, expires_in=3600):
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.add(self)
        return self.token

    def revoke_token(self):
        self.token_expiration = datetime.utcnow() - timedelta(seconds=1)

    @staticmethod
    def check_token(token):
        user = User.query.filter_by(token=token).first()
        if user is None or user.token_expiration < datetime.utcnow():
            return None
        return user
