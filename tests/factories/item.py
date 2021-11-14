import factory
import secrets
from cogs.utils.listkeeper.lkdb import (
    Item,
    Session
)


class ItemFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Item
        sqlalchemy_session = Session

    item_id = factory.LazyFunction(lambda: secrets.token_hex(4))
    name = factory.Faker("sentence", nb_words=5)
    note = factory.Faker("sentence", nb_words=10)

    collection = factory.SubFactory("factories.collection.CollectionFactory")
    collection_id = factory.SelfAttribute("collection.id")