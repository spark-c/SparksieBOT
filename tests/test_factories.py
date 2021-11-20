import pytest
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.orm.collections import InstrumentedList

import cogs.utils.listkeeper.lkdb as lkdb
from tests.factories.item import ItemFactory
from tests.factories.collection import CollectionFactory, EmptyCollectionFactory


class TestCollection:

    def test_create_new_collection(self):
        colx = CollectionFactory.create()
        assert colx


    def test_create_new_collection_with_no_items(self):
        colx = EmptyCollectionFactory.create()
        assert len(colx.items) == 0
        assert type(colx.items) is InstrumentedList


    def test_collection_has_guild_id(self):
        colx = EmptyCollectionFactory.create()
        print(f"{colx.guild_id=}")
        print(f"{colx.name=}")
        assert type(colx.guild_id) is str


    def test_new_collection_makes_it_to_database(self):
        colx = EmptyCollectionFactory.create()
        result = lkdb.get_collection_by_name(colx.name, colx.guild_id)

        assert result


class TestItem:

    def test_create_new_item(self):
        item = ItemFactory.create()
        assert item