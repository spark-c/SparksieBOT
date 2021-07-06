# manages interfacing with heroku postgres db for ListKeeper cog
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy import create_engine, ForeignKey, Column, Integer, String


engine = create_engine('postgresql://localhost/baby-bot-dev', echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)


class Collection(Base):
    __tablename__ = "collection"

    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    collection_id = Column(Integer, primary_key=True, nullable=False)
    items = relationship("Item", backref="collection", cascade="all, delete-orphan")


class Item(Base):
    __tablename__ = "item"

    name = Column(String, nullable=False)
    note = Column(String, nullable=True)
    item_id = Column(Integer, primary_key=True, nullable=False)
    collection_id = Column(Integer, ForeignKey("collection.collection_id"), nullable=False)
    # collection = relationship("Collection", back_populates="items")


Base.metadata.create_all(engine)