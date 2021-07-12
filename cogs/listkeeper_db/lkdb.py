# manages interfacing with heroku postgres db for ListKeeper cog
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine, ForeignKey, Column, Integer, String
import secrets

from typing import Union, List, Set, Any

class DatabaseError(Exception):
    def __init__(self, message="Unable to complete database operation!", object_to_debug: Any=None) -> None:
        # self.object_debug: str = object_to_debug.debug()
        # self.message: str = message + "\n" + self.object_debug
        self.message: str = message
        super().__init__(self.message)


# TODO: handle possibility of db downtime
# TODO: use envvar for db address
engine = create_engine('postgresql://localhost/baby-bot-dev', echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)


class Collection(Base):
    __tablename__ = "collection"

    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    collection_id = Column(String, primary_key=True, nullable=False)
    # items = relationship("Item", backref="collection", cascade="all, delete-orphan", lazy="joined")
    guild_id = Column(String, nullable=False)


class Item(Base):
    __tablename__ = "item"

    name = Column(String, nullable=False)
    note = Column(String, nullable=True)
    item_id = Column(String, primary_key=True, nullable=False)
    collection_id = Column(String, ForeignKey("collection.collection_id"), nullable=False)
    collection = relationship("Collection", lazy="joined", back_populates="items")

Collection.items = relationship("Item", back_populates="collection", lazy="joined")

Base.metadata.create_all(engine)
session = Session()
master_collection: List[Collection] = session.query(Collection).all()


## HELPER FUNCTIONS ##
## Create
def create_collection(name: str, description: Union[str, None], collection_id: str, guild_id: str) -> Union[Collection, None]:
    description = "" if description == None else description # default argument "" (conditional expression)
    new_colx = Collection(name=name, description=description, collection_id=collection_id, guild_id=guild_id)
    with Session() as session:
        try:
            session.add(new_colx)
            session.commit()
            master_collection.append(new_colx)
            return new_colx
        except:
            raise DatabaseError(
                "Failed to add new entry to database!\n" +
                "new_colx\n" +
                f"name: {name}\n" +
                f"description: {description}\n" +
                f"collection_id: {collection_id}\n" +
                f"guild_id: {guild_id}\n"
            )

        ## Commented the below so we will fail loudly during development
        # with session.begin(): # SessionTransaction object; automatically commit()s at end of context block if no exceptions.
        #     session.add(new_colx)


def create_item(name: str, item_id: str, collection_id: str, note: str="") -> None:
    pass


## Read
def get_guild_collections(guild_id: str) -> Union[List[Collection], None]:
    pass


def get_items(collection: Collection):# -> List[Item]:
    pass


## Update TODO


## Delete
def delete_collection(collection: Collection) -> None:
    pass


def delete_item(item: Item) -> None:
    pass


## Search
def search_collections_by_id(collection_id: str) -> Union[Collection, None]:
    for collection in master_collection:
        if collection.collection_id == collection_id:
            return collection
    return None


def search_collections_by_guild_id(guild_id: str) -> List[Collection]:
    results: List[Collection] = list()
    for collection in master_collection:
        if collection.guild_id == guild_id:
            results.append(collection)
    return results


## ID Management
tmp: List[Item] = session.query(Item).all() # These two lines create a set of all ids in use, to prevent creating duplicates
used_ids: Set[str] = set([i.collection_id for i in tmp] + [j.item_id for j in tmp])

def generate_id() -> str:
    while True: # loop until we get a unique ID
        id: str = secrets.token_hex(4)
        if id not in used_ids:
            return id