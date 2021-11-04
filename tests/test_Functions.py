import pytest
import discord.ext.test as dpytest
import random
from . import conftest


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


    @pytest.mark.asyncio
    async def test_cat_(self, cog_bot):
        pass


    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "dice, expected_roll",
        [
            ("4d6", 5),
            ("2d10", 10),
            ("12d100", 74),
            ("1d2", 2)
        ]
    )
    async def test_roll(self, cog_bot, dice, expected_roll):
        # using random.seed(), the die should roll the same number every time
        await dpytest.message(f"!roll {dice} 24601")
        await conftest.print_message_history(2)
        assert dpytest.verify().message().contains().content(
            f"Here are your numbers: {expected_roll}"
        )
    

