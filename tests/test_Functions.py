import pytest
import discord.ext.test as dpytest


@pytest.fixture
def cog_bot(bot):
    bot.load_extension("cogs.Functions")
    yield bot
    bot.unload_extension("cogs.Functions")


class TestFunctions:
    
    @pytest.mark.asyncio
    async def test_ping(self, cog_bot):
        await dpytest.message("!ping")
        assert dpytest.verify().message().content("Pong!")
