import discord
from discord.ext import commands
import requests
from typing import Union, Dict, List, Optional
from argparse import Namespace # for type annots

import utils.cmdparser as cmdparser


class ApiCalls(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def pspop(self, ctx, *args) -> None:
        server_lookup = {
            "connery": "1",
            "miller": "10",
            "cobalt": "13",
            "emerald": "17",
            "jaeger": "19",
            "soltech": "40"
        }

        try:
            pargs: Namespace = cmdparser.pspop.parse_args(args)
        except cmdparser.ArgumentError as e:
            await self.handle_argument_error(ctx, e)
            return

        if pargs.server is None:
            server_name = "emerald"
        elif pargs.server in server_lookup.keys():
            server_name = pargs.server.lower()
        else:
            await ctx.send("Server name not recognized!")
            return

        try:
            response = requests.get(f"https://ps2.fisu.pw/api/population/?world={server_lookup[server_name]}")
            data = response.json()["result"][0]
            vs = data["vs"]
            nc = data["nc"]
            tr = data["tr"]
            nso = data["ns"]
        except Exception as e:
            print(e)
            await ctx.send("There was an error!")
            return

        await ctx.send(
            f"Here is the current population for {server_name.capitalize()}:\n" +
            f"VS: {vs}\n" +
            f"NC: {nc}\n" +
            f"TR: {tr}\n" +
            f"NSO: {nso}"
        )


    async def handle_argument_error(
        self, 
        ctx, 
        error: cmdparser.ArgumentError
        ) -> None:

        # TODO fix the formatting of this message
        await ctx.channel.send(
                "Unable to parse arguments!" +
                error.message + "\n" +
                error.usage
            )
        return
        

def setup(bot):
    bot.add_cog(ApiCalls(bot))