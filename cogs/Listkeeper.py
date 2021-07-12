# Cog to keep track of lists made by users


import discord
from discord.ext import commands
import asyncio
from typing import Union, Dict, List

from cogs.listkeeper_db.lkdb import Collection
import listkeeper_db.lkdb as lkdb


class Listkeeper(commands.cog):
    
    selected_list: Union[Collection, None] = None

    def __init__(self, bot):
        self.bot = bot


    ## Create
    @commands.command
    def newlist(self, ctx, *args) -> None:
        name = args[0]
        desc = args[1] if args[1] else None
        new_colx = lkdb.create_collection(
            name=name,
            description=desc,
            collection_id=lkdb.generate_id(),
            guild_id=ctx.guild.id
        )
        Listkeeper.selected_list = new_colx


    @commands.command
    def additem(self, ctx) -> None:
        pass


    ## Read
    @commands.command
    def listall(self, ctx) -> None:
        tmp: List[Collection] = lkdb.get_guild_collections(ctx.guild.id)
        collection_names: List[str] = [colx.name for colx in tmp]
        ctx.channel.send(f"Here are your lists:\n{collection_names.join('\n')}")


    @commands.command
    def list(self, ctx) -> None:
        pass


    ## Update
    @commands.command
    def updateitem(self, ctx) -> None:
        pass


    @commands.command
    def updatelist(self, ctx) -> None:
        pass


    # Delete
    @commands.command
    def rmlist(self, ctx) -> None:
        pass


    @commands.command
    def rmitem(self, ctx) -> None:
        pass


    # Utility
    @commands.command
    def listundo(self, ctx) -> None:
        pass


def setup(bot):
    bot.add_cog(Listkeeper(bot))

    


    


    
    


    
