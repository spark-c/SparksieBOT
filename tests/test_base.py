import pytest
import discord.ext.test as dpytest
import random
from typing import List
from discord import TextChannel, Message

from utils import groovycommands


@pytest.fixture
def bot_base(bot):
    bot_no_cogs = bot()
    return bot_no_cogs


class TestOnMessage:

    @pytest.mark.asyncio
    async def test_bot_replies_to_glory(self, bot_base):
        await dpytest.message("glory")
        assert dpytest.verify().message().contains().content("Glory!")


    @pytest.mark.asyncio
    async def test_glory_has_cooldown(self, bot_base):
        await dpytest.message("glory")
        await dpytest.message("glory")
        history = await dpytest.get_config().channels[0].history().flatten() #type: ignore
        assert len(history) == 3


    @pytest.mark.asyncio
    async def test_reply_to_groovy(self, bot_base):
        await dpytest.message("groovy")
        assert dpytest.verify().message().content("...")


    @pytest.mark.asyncio
    async def test_congratulations(self, bot_base):
        prompts = [
            "congratulations!",
            "Congrats!",
            "congrats",
            "CONGRATS"
        ]
        for prompt in prompts:
            assert "congrat" in prompt.lower()
        await dpytest.message(random.choice(prompts))
        assert dpytest.verify().message().contains().content(":confetti_ball:")


    @pytest.mark.asyncio
    async def test_deletes_music_commands(self, bot_base):
        cmd = groovycommands.groovycommands[0]
        await dpytest.message(cmd)

        channel: TextChannel = dpytest.get_config().channels[0] # type: ignore
        history:List[Message] = await channel.history(limit=2).flatten()
        contents: List[str] = [msg.content for msg in history]

        assert not cmd in contents
        assert "No littering" in contents[-1]
        # TODO: add test for pinging in music channel "where it belongs"


    class TestPausing:

        @pytest.mark.asyncio
        async def test_pause_commands(self, bot_base):
            pass


        @pytest.mark.asyncio
        async def test_pause_events(self, bot_base):
            pass

        
        @pytest.mark.asyncio
        async def test_pauses_only_one_guild(self, bot_base):
            pass


        @pytest.mark.asyncio
        async def test_unpause(self, bot_base):
            pass