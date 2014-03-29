from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///:memory:')
Base = declarative_base()

class Posty(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    data = Column(String)

    def __init__(self, data):
        self.data = data


    def __repr__(self):
        return "<Posty %s>" % self.data


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)


def store_post(data):
    session = Session()
    p = Posty(data)
    session.add(p)
    session.commit()


def list_posts():
    session = Session()
    return session.query(Posty).all()
