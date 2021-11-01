# used to configure pytest / for use with dpytest

import pytest
import discord.ext.test as dpytest
import os
from setuptools import glob

import baby_bot


@pytest.fixture
def bot(event_loop):
    bot = baby_bot.SparksieBot(
        command_prefix="!", intents=baby_bot.intents, loop=event_loop
    )
    baby_bot.initialize_bot(bot)
    dpytest.configure(bot)
    return bot


# Cleans up leftover files generated through dpytest
def pytest_sessionfinish():
    # Clean up attachment files
    files = glob.glob('./dpytest_*.dat')
    for path in files:
        try:
            os.remove(path)
        except Exception as e:
            print(f"Error while deleting file {path}: {e}")