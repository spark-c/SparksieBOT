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
#     loop = asyncio.get_event_loop()
#     yield loop
#     loop.close()


@pytest.fixture()
async def bot(event_loop):
    
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
def patched_request(monkeypatch):
    class MockedResponse:
        def __init__(self, url, status_code=200, **kwargs):
            self.status_code = status_code
            self.url = url
            self.text = self.json()['text']
            self.kwargs = kwargs
        
        def json(self):
            return patch_cfg.lookup[self.url]

        def raise_for_status(self):
            if self.status_code != 200:
                raise requests.HTTPError(f"Mocked Error: {self.status_code}")
            return None

    def mock_get(url, **kwargs):
        return MockedResponse(url, **kwargs)

    monkeypatch.setattr(requests, "get", mock_get)


@pytest.fixture
def patched_request_404(monkeypatch, patched_request):
    def mock_get_404(url, **kwargs):
        return MockedResponse(url, status_code=404) #type: ignore

    monkeypatch.setattr(requests, "get", mock_get_404)


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