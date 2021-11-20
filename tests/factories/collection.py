import factory
import secrets
from sqlalchemy.orm.collections import InstrumentedList

from cogs.utils.listkeeper.lkdb import Session
from cogs.utils.listkeeper.models import Collection
from .item import ItemFactory


class CollectionFactoryBase(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Collection
        sqlalchemy_session = Session

    id = factory.LazyFunction(lambda: secrets.token_hex(4))
    name = factory.Faker("sentence", nb_words=5)
    description = factory.Faker("sentence", nb_words=10)
    guild_id = factory.LazyFunction(
        lambda: str(
            factory.Faker(
                "pyint",
                # mimicks the dpytest guild.id range, but with leading 8 instead of 9
                min_value=8095_0000_0000_0000_00,
                max_value=8199_9999_9999_9999_99,
            )
        )
    )


class CollectionFactory(CollectionFactoryBase):
    @factory.post_generation
    def populate_items(self, create, extracted, **kwargs):
        if not create:
            return
        # if extracted:
        #     pass
        ItemFactory.create(collection=self)


class EmptyCollectionFactory(CollectionFactoryBase):
    items = InstrumentedList()