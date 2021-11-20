# manages interfacing with heroku postgres db for ListKeeper cog

import secrets
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker, scoped_session
from typing import Union, List, Set

from .models import Collection, Item, engine
from .errors import DatabaseError

# TODO: handle possibility of db downtime

# https://docs.sqlalchemy.org/en/14/orm/contextual.html#unitofwork-contextual
session_factory = sessionmaker(bind=engine, expire_on_commit=False)
Session = scoped_session(session_factory)

## HELPER FUNCTIONS ##
## Create
def create_collection(name: str, description: Union[str, None], id: str, guild_id: str) -> Collection:
    description = "" if description == None else description # default argument "" (conditional expression)
    new_colx = Collection(name=name, description=description, id=id, guild_id=guild_id)
    with Session() as session:
        try:
            session.add(new_colx)
            session.commit()
            return new_colx
        except:
            raise DatabaseError(
                "Failed to add new entry to database!\n" +
                "new_colx\n" +
                f"name: {name}\n" +
                f"description: {description}\n" +
                f"collection_id: {id}\n" +
                f"guild_id: {guild_id}\n"
            )


def create_item(name: str, note: Union[str, None], id: str, collection_id: str) -> Item:
    note = "" if note is None else note
    new_item: Item = Item(name=name, note=note, id=id, collection_id=collection_id)
    with Session() as session:
        try:
            session.add(new_item)
            session.commit()
        except:
            raise DatabaseError(
                "Failed to add new entry to database!\n" +
                "new_item\n" +
                f"name: {name}\n" +
                f"note: {note}\n" +
                f"item_id: {id}\n" +
                f"collection_id: {collection_id}\n"
            )
    return new_item


## Read
def get_guild_collections(guild_id: str) -> List[Collection]:
    with Session() as session:
        results: List[Collection] = (
            session.query(Collection)
            .filter(Collection.guild_id==guild_id)
            .all()
        )
    
    if not results:
        raise DatabaseError("No results found!")

    return results


def get_collection_by_name(name: str, guild_id: str) -> Collection:
    with Session() as session:
        result: Collection = (
            session.query(Collection)
            .filter(func.lower(Collection.name) == name.lower())
            .filter(Collection.guild_id == guild_id)
            .first()
        )

    if result is None:
        raise DatabaseError(f"Collection '{name}' not found!")

    return result


def get_items(collection_name: str, guild_id: str) -> List[Item]:
    try:
        found_colx: Union[Collection, None] = get_collection_by_name(collection_name, guild_id)
    except DatabaseError as e:
        raise DatabaseError(e)

    with Session() as session:
        results: List[Item] = (
            session.query(Item)
            .filter(Item.collection_id == found_colx.id)
            .all()
        )

    if not results:
        raise DatabaseError(f"No items found for collection '{collection_name}'!")

    return results


## Update TODO


## Delete
def delete_collection_by_name(name: str, guild_id: str) -> None:
    try:
        colx_to_delete: Collection = (
            get_collection_by_name(name=name, guild_id=guild_id)
        )
    except DatabaseError as e:
        raise DatabaseError(e)

    try:
        with Session() as session: 
            session.delete(colx_to_delete)
            session.commit()
    except:
        raise DatabaseError()


def delete_item(collection_name: str, guild_id: str, item_name: str) -> None:
    with Session() as session:
        try:
            parent_collection: Collection = (
                get_collection_by_name(name=collection_name, guild_id=guild_id)
            )
        except DatabaseError as e:
            raise DatabaseError(e)
        
        # TODO abstract this into its own function
        item_to_delete: Item = (
            session.query(Item)
            .filter(Item.collection_id==parent_collection.id)
            .filter(func.lower(Item.name)==item_name.lower())
            .first()
        )
        if item_to_delete is None:
            raise DatabaseError(f"Item {item_name} not found!")

        try:
            session.delete(item_to_delete)
            session.commit()
        except:
            raise DatabaseError(f"Unable to delete item '{item_name}'")


## ID Management
with Session() as session:
    tmp: List[Item] = session.query(Item).all() # These two lines create a set of all ids in use, to prevent creating duplicates
    used_ids: Set[str] = set([item.collection_id for item in tmp] + [item.id for item in tmp])

def generate_id() -> str:
    while True: # loop until we get a unique ID
        id: str = secrets.token_hex(4)
        if id not in used_ids:
            used_ids.add(id)
            return id