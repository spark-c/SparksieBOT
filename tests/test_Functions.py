import pytest
import discord.ext.test as dpytest
from discord import Embed
import random
import requests
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
        await dpytest.message("!marco")
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
        await dpytest.message(f"!roll {dice} --test")
        assert dpytest.verify().message().contains().content(
            f"Here are your numbers: {expected_roll}"
        )

    
    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "dice, err_msg",
        [
            ("4", "Usage: !roll 4d6"),
            ("2 10", "Usage: !roll 4d6"),
            ("-1d4", "Values must be greater than zero!"),
            ("5d-10", "Values must be greater than zero!"),
            ("5a20", "Usage: !roll 4d6")
        ],
        ids=[
            "single-digit",
            "no-letter-btwn",
            "negative-value1",
            "negative-value2",
            "wrong-letter-separator"
        ]
    )
    async def test_roll_with_bad_values(self, cog_bot, dice, err_msg):
        await dpytest.message(f"!roll {dice} 24601")
        assert dpytest.verify().message().content(err_msg)
    

    @pytest.mark.asyncio
    async def test_teampicker_(self, cog_bot):
        pass


    @pytest.mark.asyncio
    async def test_say(self, cog_bot):
        pass


    @pytest.mark.asyncio
    async def test_sleepy(self, cog_bot):
        pass


    @pytest.mark.asyncio
    async def test_lotr_returns_correct_embed(self, cog_bot, patched_request):
        test_embed = Embed(
            name="",
            description="\"The world is indeed full of peril, and in it there are many dark places; but still there is much that is fair, and though in all lands love is now mingled with grief, it grows perhaps the greater.\""
        )
        test_embed.add_field(
            name="Haldir",
            value="J.R.R. Tolkien, Lothlórien, The Fellowship of the Ring"
        )

        await dpytest.message("!lotr --test")
        assert dpytest.verify().message().embed(test_embed)

    
    @pytest.mark.asyncio
    async def test_lotr_404_case(self, cog_bot, patched_request_404):
        await dpytest.message("!lotr --test")
        assert dpytest.verify().message().content("I couldn't find a quote!")
