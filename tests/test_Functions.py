import pytest
import discord.ext.test as dpytest


@pytest.fixture
def cog_bot(bot):
    bot_with_cog = bot(["Functions"])
    return bot_with_cog

    
class TestOnMessage:

    @pytest.mark.asyncio
    async def test_reply_to_good_bot(self, cog_bot):
        await dpytest.message("good bot")
        assert dpytest.verify().message().content("Thanks!")


    @pytest.mark.asyncio
    async def test_reply_to_mention(self, cog_bot):
        await dpytest.message(cog_bot.user.mention)
        assert dpytest.verify().message().content("Beep boop!")


    @pytest.mark.asyncio
    async def test_reply_to_hi_and_mention(self, cog_bot):
        message = await dpytest.message(f"hi {cog_bot.user.mention}")
        assert dpytest.verify().message().content(f"Hello {message.author}!")


class TestCommands:

    @pytest.mark.asyncio
    async def test_ping(self, cog_bot):
        await dpytest.message("!ping")
        assert dpytest.verify().message().content("Pong!")


    @pytest.mark.asyncio
    async def test_marco_with_one_TextChannel(self, cog_bot):
        message = await dpytest.message("!marco")
        assert dpytest.verify().message().content("Polo!")


    @pytest.mark.asyncio
    async def test_marco_with_multiple_TextChannels(self, cog_bot):
        dpytest.get_config()
