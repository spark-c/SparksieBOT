import pytest
import discord.ext.test as dpytest
from discord import Embed, Message
from discord.abc import GuildChannel
from discord.iterators import _AsyncIterator
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine

from cogs.utils.listkeeper.models import get_db_url, engine
from cogs.utils.listkeeper.models import Collection, Item
from . import conftest

from typing import List

from tests.factories.item import ItemFactory
from tests.factories.collection import CollectionFactory


session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)


@pytest.fixture
def cog_bot(bot):
    bot_with_cog = bot(["Listkeeper"])
    return bot_with_cog


async def get_last_message():
    channel: GuildChannel = dpytest.get_config().channels[0]
    history: List[Message] = await channel.history(limit=1).flatten() #type: ignore
    return history[0]


class TestNewlist:

    @pytest.mark.asyncio
    async def test_bot_reacts_to_command_message(self, cog_bot):
        await dpytest.message("!newlist 'My Test List' 'My test description'")
        msg = await get_last_message()
        await dpytest.add_reaction(dpytest.get_config().members[0], msg, ":joy:")
        print(f"{msg.reactions=}")
        # assert msg == 1
        assert False


    @pytest.mark.asyncio
    async def test_create_new_list(self, cog_bot):
        await dpytest.message("!newlist 'My Test List' 'My test description'")
        # colx = CollectionFactory.create()
        with Session() as session:
            output = session.query(Collection).first()
            print(f"{output=}")
        assert True
        