import pytest
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from tests.factories.item import ItemFactory
from tests.factories.collection import CollectionFactory


class TestCollection:

    def test_create_new_collection(self):
        colx = CollectionFactory.create()
        assert colx


class TestItem:

    def test_create_new_item(self):
        item = ItemFactory.create()
        assert item