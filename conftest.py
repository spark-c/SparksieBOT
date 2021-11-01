# used to configure pytest / for use with dpytest

import pytest
import discord.ext.test as dpytest
import os
from setuptools import glob

import bot as sb


@pytest.fixture
def bot(event_loop):
    bot = sb.SparksieBot(
        command_prefix="!", intents=sb.intents, loop=event_loop
    )
    sb.initialize_bot(bot)
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