from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from app import db

engine = create_engine('infogeneral.db', echo=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

# Set your classes here.

'''
class User(Base):
    __tablename__ = 'Users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(30))

    def __init__(self, name=None, password=None):
        self.name = name
        self.password = password
'''

# Create tables.
# Base.metadata.create_all(bind=engine)


class User(UserMixin):

    def __init__(self, id, name, usr, pwd, is_admin=False):
        self.id = id
        self.name = name
        self.usr = usr
        self.pwd = generate_password_hash(pwd)
        self.is_admin = is_admin

    def set_password(self, pwd):
        self.pwd = generate_password_hash(pwd)

    def check_password(self, pwd):
        return check_password_hash(self.pwd, pwd)

    def __repr__(self):
        return '<User {}>'.format(self.usr)


# users = [[1, "santiago", "santiagouser", "santiago123", False],[2, "camilo", "camilouser", "camilo123", True]]
users = [{'id': 1, 'name': 'santiago', 'usr': 'santiagouser',
          'pwd': 'santiago123', 'is_Admin': True}]


def get_user(usr):
    for user in users:
        if user['usr'] == usr:
            return user
    return None
