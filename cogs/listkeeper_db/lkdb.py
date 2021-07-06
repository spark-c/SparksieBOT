# manages interfacing with heroku postgres db for ListKeeper cog
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy import create_engine, ForeignKey, Column, Integer, String

from typing import Union, List


# TODO: handle possibility of db downtime
# TODO: use envvar for db address
engine = create_engine('postgresql://localhost/baby-bot-dev', echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)


class Collection(Base):
    __tablename__ = "collection"

    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    collection_id = Column(Integer, primary_key=True, nullable=False)
    items = relationship("Item", backref="collection", cascade="all, delete-orphan")
    #TODO guild_id = Column(Integer, nullable=False)


class Item(Base):
    __tablename__ = "item"

    name = Column(String, nullable=False)
    note = Column(String, nullable=True)
    item_id = Column(Integer, primary_key=True, nullable=False)
    collection_id = Column(Integer, ForeignKey("collection.collection_id"), nullable=False)
    # collection = relationship("Collection", back_populates="items")


Base.metadata.create_all(engine)

## HELPER FUNCTIONS ##

## Create
def create_collection(name: str, collection_id: int, guild_id: int, description: str="") -> None:
    pass


def create_item(name: str, item_id: int, collection_id: int, note: str="") -> None:
    pass


## Read
def get_guild_collections(guild_id: int) -> List[Collection[Item]]:
    pass


def get_items(collection: Collection) -> List[Item]:
    pass


## Update TODO


## Delete
def delete_collection(collection: Collection) -> None:
    pass


def delete_item(item: Item) -> None:
    pass