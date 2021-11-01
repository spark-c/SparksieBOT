import pytest
import discord.ext.test as dpytest
# import baby_bot

# def test_bot_has_set(bot):
#     assert type(bot.paused_guilds) == set


# @pytest.mark.asyncio
# async def test_ping(bot):
    # bot.load_extension("cogs.Functions")
    # assert bool(dpytest.verify().message().contains().content("extension"))
    # await dpytest.message("!ping")
    # assert dpytest.verify().message().contains().content("Pong!")


@pytest.mark.asyncio
async def test_bot_replies_to_glory(bot):
    await dpytest.message("glory")
    assert dpytest.verify().message().contains().content("lory")

# @pytest.mark.asyncio
# async def test_functions(bot):
#     await dpytest.message("!load Functions")
#     await dpytest.message("!ping")
#     assert dpytest.verify().message().contains().content("Pong")