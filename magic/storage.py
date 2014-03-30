import hashlib
from contextlib import contextmanager
from sqlalchemy import Column, Integer, String, create_engine, inspect
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import IntegrityError

salt = 'sodium chloride'

engine = create_engine('sqlite:///:memory:')
Base = declarative_base()
session = sessionmaker(bind=engine)()


class User(Base):
    __tablename__ = "users"

    username = Column(String, primary_key=True)
    hashword = Column(String)

    def __init__(self, username, hashword):
        self.username = username
        self.hashword = hashword

    def __repr__(self):
        return "<User %s>" % self.username

    def set_password(self, password):
        self.hashword = _make_hashword(password)


def init_db():
    Base.metadata.create_all(engine)


def _make_hashword(password):
    sha = hashlib.sha256()
    sha.update(password.encode())
    sha.update(salt.encode())
    return sha.hexdigest()


def create_user(username, password):
    '''Create a user with the given username and password.
    Hash and salt the passwords. Mmmm, delicious salt.

    '''
    session.add(User(username, _make_hashword(password)))
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise ValueError("Username '%s' already exists" % username)


def get_user(username):
    '''Return the user that corresponds to the given username.
    If no user exists with that name, return None.

    '''
    return session.query(User).filter_by(username=username).first()


def update_user(user):
    '''Update the user that was passed in, except the username.'''
    hist = inspect(user).attrs.username.history
    if hist.has_changes():
        user.username = hist.deleted[0]
    session.add(user)
    session.commit()
