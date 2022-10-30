import os
import json
from typing import Union
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine, ForeignKey, Column, String, func

from .errors import DatabaseError


def get_db_url():
    # config / envvars
    DATABASE_URL: Union[str, None] = None
    try:
        with open("./config.json") as f:
            # this creates an in-memory sqlite3 db
            DATABASE_URL = json.load(f)["DATABASE_URL"]["development"]
    except: # when hosted from Heroku / envvars
        DATABASE_URL = os.environ["DATABASE_URL"].replace("postgres", "postgresql") # Heroku demands "postgres" instead of "postgresql"

    return DATABASE_URL


Base = declarative_base()
db_url = get_db_url()
try:
    engine = create_engine(db_url, echo=False)
except:
    raise DatabaseError(f"Unable to connect to the database! Address used: {db_url}")


class Collection(Base):
    __tablename__ = "collection"

    id = Column(String, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    items = relationship("Item", back_populates="collection", lazy="joined", cascade="all, delete-orphan")
    guild_id = Column(String, nullable=False)


class Item(Base):
    __tablename__ = "item"

    id = Column(String, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    note = Column(String, nullable=True)
    collection_id = Column(String, ForeignKey("collection.id"), nullable=False)
    collection = relationship("Collection", lazy="joined", back_populates="items")


Base.metadata.create_all(engine)
