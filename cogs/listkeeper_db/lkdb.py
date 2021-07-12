# manages interfacing with heroku postgres db for ListKeeper cog
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy import create_engine, ForeignKey, Column, Integer, String
import secrets

from typing import Union, List, Any

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
    collection_id = Column(Integer, primary_key=True, nullable=False)
    items = relationship("Item", backref="collection", cascade="all, delete-orphan")
    guild_id = Column(Integer, nullable=False)


class Item(Base):
    __tablename__ = "item"

    name = Column(String, nullable=False)
    note = Column(String, nullable=True)
    item_id = Column(Integer, primary_key=True, nullable=False)
    collection_id = Column(Integer, ForeignKey("collection.collection_id"), nullable=False)
    # collection = relationship("Collection", back_populates="items")


master_collection: List[Collection] = []
Base.metadata.create_all(engine)
session = Session()


## HELPER FUNCTIONS ##
## Create
def create_collection(name: str, description: str, collection_id: int, guild_id: int) -> Union[Collection, None]:
    description = "" if description == None else description # default argument "" (conditional expression)
    new_colx = Collection(name=name, description=description, collection_id=collection_id, guild_id=guild_id)
    with Session() as session:
        try:
            session.add(new_colx)
            session.commit()
            master_collection.append(new_colx)
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


def create_item(name: str, item_id: int, collection_id: int, note: str="") -> None:
    pass


## Read
def get_guild_collections(guild_id: int) -> List[Collection]:
    pass


def get_items(collection: Collection) -> List[Item]:
    pass


## Update TODO


## Delete
def delete_collection(collection: Collection) -> None:
    pass


def delete_item(item: Item) -> None:
    pass


## Search
def search_collections_by_id(collection_id: int) -> Union[Collection, None]:
    for collection in master_collection:
        if collection.collection_id == collection_id:
            return collection
    return None



## ID Management
tmp = session.query(Item).all() # These two lines create a set of all ids in use, to prevent creating duplicates
used_ids = set([i.collection_id for i in tmp] + [j.item_id for j in tmp])
print("Used IDs:", used_ids)

def generate_id():
    while True: # loop until we get a unique ID
        id = secrets.token_hex(4)
        if id not in used_ids:
            return id