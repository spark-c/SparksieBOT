import factory
import secrets
from cogs.utils.listkeeper.lkdb import Session
from cogs.utils.listkeeper.models import Item


class ItemFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Item
        sqlalchemy_session = Session

    id = factory.LazyFunction(lambda: secrets.token_hex(4))
    name = factory.Faker("sentence", nb_words=5)
    note = factory.Faker("sentence", nb_words=10)

    collection = factory.SubFactory("tests.factories.collection.CollectionFactory")
    collection_id = factory.SelfAttribute("collection.id")