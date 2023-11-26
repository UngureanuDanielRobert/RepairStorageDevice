import sqlalchemy.orm
from flask_login import UserMixin

from init import db


class User(db.Model,UserMixin):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)  # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))


class Fisier(db.Model):
    __tablename__ = 'Fisier'
    fisierid = db.Column(db.Integer, primary_key=True)
    calefisier = db.Column(db.String(2500))
    userid = sqlalchemy.orm.mapped_column(db.Integer,sqlalchemy.ForeignKey('User.id'))

