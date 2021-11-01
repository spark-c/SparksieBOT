import pytest
import discord.ext.test as dpytest


class TestOnMessageEvents:

    @pytest.mark.asyncio
    async def test_bot_replies_to_glory(self, bot):
        await dpytest.message("glory")
        assert dpytest.verify().message().contains().content("Glory!")


    @pytest.mark.asyncio
    async def test_glory_has_cooldown(self, bot):
        """ Should not reply with Glory! here because of cooldown. """
        await dpytest.message("glory")
        assert not dpytest.verify().message().contains().content("Glory!")


    @pytest.mark.asyncio
    async def test_reply_to_groovy(self, bot):
        await dpytest.message("groovy")
        assert dpytest.verify().message().contains().content("...")