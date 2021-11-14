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
        try:

            response = requests.get("https://ps2.fisu.pw/api/population/?world=17")
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
            "Here is the current population for Emerald:\n" +
            f"VS: {vs}\n" +
            f"NC: {nc}\n" +
            f"TR: {tr}\n" +
            f"NSO: {nso}"
        )
        

def setup(bot):
    bot.add_cog(ApiCalls(bot))