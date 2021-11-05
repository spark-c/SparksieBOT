# used to configure pytest / for use with dpytest

import pytest
import discord.ext.test as dpytest
import asyncio
import os
import requests
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
    def mock_get(url, **kwargs):
        json = patch_cfg.lookup[url]
        mock = type("MockedRequest", (), {})()
        mock.json = json #type: ignore
        mock.text = mock.json['text'] #type: ignore
        return mock

    monkeypatch.setattr(requests, "get", mock_get)


@pytest.fixture
def patched_request_success(monkeypatch, patched_request):
    def mock_status_success():
        return None

    monkeypatch.setattr(requests.Response, "raise_for_status", mock_status_success)


@pytest.fixture
def patched_request_404(monkeypatch, patched_request):
    def mock_raise_for_status_404():
        raise requests.HTTPError("Mock 404 Error")

    monkeypatch.setattr(requests.Response, "raise_for_status", mock_raise_for_status_404)


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