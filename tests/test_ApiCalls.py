import pytest
import discord.ext.test as dpytest
from discord import Embed
from . import conftest


@pytest.fixture
def cog_bot(bot):
    bot_with_cog = bot(["ApiCalls"])
    return bot_with_cog



class TestPspop:
    @pytest.mark.asyncio
    async def test_pspop_default(self, cog_bot, patched_request):
        await dpytest.message("!pspop")
        assert dpytest.verify().message().content(
            "Here is the current population for Emerald:\n" +
            "VS: 99\n" +
            "NC: 99\n" +
            "TR: 99\n" +
            "NSO: 99"
        )


    @pytest.mark.parametrize(
        "args, server",
        [
            ("--server connery", "connery"),
            ("-s connery", "connery"),
            ("-s miller", "miller")
        ]
    )
    @pytest.mark.asyncio
    async def test_pspop_server_flag(self, cog_bot, patched_request, args, server):
        await dpytest.message(f"!pspop {args}")
        assert dpytest.verify().message().contains().content(server.capitalize())


    @pytest.mark.asyncio
    async def test_handles_unknown_flag(self, cog_bot, patched_request_404):
        # TODO
        assert True


    @pytest.mark.asyncio
    async def test_handles_unknown_server(self, cog_bot, patched_request_404):
        # TODO
        assert True


    @pytest.mark.asyncio
    async def test_pspop_network_error(self, cog_bot, patched_request_404):
        # TODO
        assert True
