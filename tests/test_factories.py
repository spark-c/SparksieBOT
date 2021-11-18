import pytest
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from tests.factories.item import ItemFactory
from tests.factories.collection import CollectionFactory


class TestCollection:

    @pytest.mark.asyncio
    def test_create_new_collection(self):
        x = CollectionFactory.create()
        assert x