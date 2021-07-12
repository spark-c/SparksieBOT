# Cog to keep track of lists made by users
# July 2021
# Collin Sparks

import discord
from discord.ext import commands
import asyncio
from typing import Union, Dict, List

try:
    from cogs.listkeeper_db.lkdb import Collection
    import cogs.listkeeper_db.lkdb as lkdb
except Exception as e:
    print(e)


class Listkeeper(commands.Cog):
    
    selected_list: Union[Collection, None] = None

    def __init__(self, bot):
        self.bot = bot


    ## Create
    @commands.command()
    async def newlist(self, ctx, *args) -> None:
        name: str = args[0]
        desc: Union[str, None] = args[1] if args[1] else None
        new_colx = lkdb.create_collection(
            name=name,
            description=desc,
            collection_id=lkdb.generate_id(),
            guild_id=ctx.guild.id
        )
        Listkeeper.selected_list = new_colx


    @commands.command()
    async def additem(self, ctx) -> None:
        pass


    ## Read
    @commands.command()
    async def listall(self, ctx) -> None:
        tmp: List[Collection] = lkdb.search_collections_by_guild_id(str(ctx.guild.id))
        if tmp:
            collection_names: str = [colx.name for colx in tmp].join("\n")
            await ctx.channel.send(f"Here are your lists:\n{collection_names}")
        else:
            await ctx.channel.send("No lists found!")


    @commands.command()
    async def list(self, ctx) -> None:
        pass


    ## Update
    @commands.command()
    async def updateitem(self, ctx) -> None:
        pass


    @commands.command()
    async def updatelist(self, ctx) -> None:
        pass


    # Delete
    @commands.command()
    async def rmlist(self, ctx) -> None:
        pass


    @commands.command()
    async def rmitem(self, ctx) -> None:
        pass


    # Utility
    @commands.command()
    async def listundo(self, ctx) -> None:
        pass


def setup(bot):
    bot.add_cog(Listkeeper(bot))

    


    


    
    


    
