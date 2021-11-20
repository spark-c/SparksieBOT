from discord import guild
from discord.channel import TextChannel
from discord.guild import Guild
from discord.member import Member
import pytest
import discord.ext.test as dpytest
from discord import Embed, Message
from discord.abc import GuildChannel
from discord.iterators import _AsyncIterator
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from sqlalchemy.orm.collections import InstrumentedList

from cogs.utils.listkeeper.models import get_db_url, engine
from cogs.utils.listkeeper.models import Collection, Item
import cogs.utils.listkeeper.lkdb as lkdb
from . import conftest

from tests.factories.item import ItemFactory
from tests.factories.collection import CollectionFactory, EmptyCollectionFactory

from typing import List


session_factory: sessionmaker = sessionmaker(bind=engine)
Session: scoped_session = scoped_session(session_factory)


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
    async def test_create_new_list(self, cog_bot):
        await dpytest.message("!newlist \"My Test List\" \"My test description\"")

        guild_id: str = str(dpytest.get_config().guilds[0].id)
        new_colx: Collection = lkdb.get_collection_by_name(
            name="My Test List",
            guild_id=guild_id
        )
        
        assert new_colx.name == "My Test List" and new_colx.description == "My test description"


    @pytest.mark.asyncio
    async def test_create_new_item(self, cog_bot):
        guild_id: str = str(dpytest.get_config().guilds[0].id)
        colx: Collection = EmptyCollectionFactory.create(guild_id=guild_id)


        result: Collection = lkdb.get_collection_by_name(colx.name, guild_id)

        await dpytest.message(
            f"!listall"# -l \"{colx.name}\" \"My new item\" \"My new note\""
        )

        await conftest.print_message_history()
        assert result is not None

        # item: Item = lkdb.get_items(colx.name, guild_id)[0]

        # assert item.name == "My new item" and item.note == "My new note"
        