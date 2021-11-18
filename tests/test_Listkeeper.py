import pytest
import discord.ext.test as dpytest
from discord import Embed
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from cogs.utils.listkeeper.models import get_db_url
from . import conftest

from tests.factories.item import ItemFactory
from tests.factories.collection import CollectionFactory


@pytest.fixture
def cog_bot(bot):
    bot_with_cog = bot(["Listkeeper"])
    return bot_with_cog


async def get_last_message():
    channel = dpytest.get_config().channels[0]
    history = await channel.history(limit=limit).flatten() #type: ignore
    return history[-1]