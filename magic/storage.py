import hashlib
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import IntegrityError

salt = 'sodium chloride'

engine = create_engine('sqlite:///:memory:')
Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    username = Column(String, primary_key=True)
    hashword = Column(String)

    def __init__(self, username, hashword):
        self.username = username
        self.hashword = hashword


    def __repr__(self):
        return "<User %s>" % self.username

Session = sessionmaker(bind=engine)


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
    session = Session()
    session.add(User(username, _make_hashword(password)))
    try:
        session.commit()
    except IntegrityError:
        raise ValueError("Username '%s' already exists" % username)


def get_user(username):
    '''Return the user that corresponds to the given username.
    If no user exists with that name, return None.

    '''
    session = Session()
    return session.query(User).filter_by(username=username).first()
