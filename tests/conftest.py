# used to configure pytest / for use with dpytest

import pytest
import discord.ext.test as dpytest
import asyncio
import os
import requests
from requests import status_codes
from setuptools import glob

import bot as sb
from .data import patch_cfg


# @pytest.fixture(scope="session")
# def event_loop():
#     """ Provides an asyncio event_loop used to session-scope the fixtures """
#     loop = asyncio.get_event_loop()
#     yield loop
#     loop.close()


@pytest.fixture()
async def bot(event_loop):
    """ Yields a function which can create a bot. Each test_Cog file will use the below factory function to specify which cog to load. """
    def _bot_factory(load_cogs=[]):
        bot = sb.SparksieBot(
            command_prefix="!", intents=sb.intents, loop=event_loop
        )
        sb.initialize_bot(bot, load_cogs)
        dpytest.configure(bot)
        return bot

    yield _bot_factory

    await dpytest.empty_queue()


@pytest.fixture
def mocked_response():
    """ Returns a factory function which further fixtures may use to create MockedResponse objects by passing in a URL and status code. """
    def _mocked_response_factory(url, status_code=200, **kwargs):
        class MockedResponse:
            def __init__(self, url, status_code, **kwargs):
                self.status_code = status_code
                self.url = url
                self.kwargs = kwargs
            
            def json(self):
                return patch_cfg.lookup[self.url]

            def raise_for_status(self):
                if self.status_code != 200:
                    raise requests.HTTPError(f"Mock Error: {self.status_code}")
                return None

        return MockedResponse(url, status_code, **kwargs)
    return _mocked_response_factory


@pytest.fixture
def patched_request(monkeypatch, mocked_response):
    """ Replaces requests.get() with a mocked success case. """
    def mock_get(url, **kwargs):
        return mocked_response(url, status_code=200, **kwargs)

    monkeypatch.setattr(requests, "get", mock_get)


@pytest.fixture
def patched_request_404(monkeypatch, mocked_response):
    """ Replaces requests.get() with a mocked failure (404) case """
    def mock_get_404(url, **kwargs):
        return mocked_response(url, status_code=404, **kwargs) 

    monkeypatch.setattr(requests, "get", mock_get_404)


async def print_message_history(limit:int=2):
    """ used to debug / manually verify message history """
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