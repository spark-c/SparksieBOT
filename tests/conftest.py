# used to configure pytest / for use with dpytest

import pytest
import discord.ext.test as dpytest
import asyncio
import os
from setuptools import glob

import bot as sb


# @pytest.fixture(scope="session")
# def event_loop():
#     loop = asyncio.get_event_loop()
#     yield loop
#     loop.close()


@pytest.fixture()
async def bot(event_loop):
    bot = sb.SparksieBot(
        command_prefix="!", intents=sb.intents, loop=event_loop
    )
    sb.initialize_bot(bot, load_cogs=[])
    dpytest.configure(bot)
    yield bot

    await dpytest.empty_queue()


async def print_message_history(limit:int=2):
    channel = dpytest.get_config().channels[0] # type: ignore
    history = await channel.history(limit=limit).flatten() # type: ignore
    contents = [msg.content for msg in history]
    print(contents)


# Cleans up leftover files generated through dpytest
def pytest_sessionfinish():
    # Clean up attachment files
    files = glob.glob('./dpytest_*.dat')
    for path in files:
        try:
            os.remove(path)
        except Exception as e:
            print(f"Error while deleting file {path}: {e}")