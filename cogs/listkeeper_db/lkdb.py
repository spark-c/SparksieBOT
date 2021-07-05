# manages interfacing with heroku postgres db for ListKeeper cog
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import declarative_base, create_engine, Column, Integer, String

engine = create_engine('sqlite:///:memory:', echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)

class Collection(Base):

    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    collection_id = Column(Integer, primary_key=True, nullable=False)
    items = relationship("Items", backref="Collection", cascade="all, delete-orphan")


class Items(Base):

    name = Column(String, nullable=False)
    note = Column(String, nullable=True)
    item_id = Column(Integer, primary_key=True, nullable=False)
    collection_id = Column(Integer, ForeignKey("Collection.collection_id"), nullable=False)