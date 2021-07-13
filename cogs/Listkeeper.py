# Cog to keep track of lists made by users
# July 2021
# Collin Sparks

import discord
from discord.ext import commands
import asyncio
from typing import Union, Dict, List

try:
    from cogs.listkeeper_db.lkdb import Collection, Item
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
        new_colx: Union[Collection, None] = lkdb.create_collection(
            name=name,
            description=desc,
            collection_id=lkdb.generate_id(),
            guild_id=ctx.guild.id
        )
        if new_colx:
            Listkeeper.selected_list = new_colx
            await ctx.channel.send(f"Successfully created {new_colx.name}!")
        else:
            await ctx.channel.send("Could not create list!")


    @commands.command()
    async def additem(self, ctx, *args) -> None:
        ## Check if list name is passed
        if args[0].startswith("-"):
            # handle misuse
            if len(args) > 3:
                await ctx.channel.send("Usage: !additem [-l <listname>] <item-name> [<item-note>]")
                return

            if args[0].tolower() not in ["-l", "-list"]:
                await ctx.channel.send(f"Invalid argument: {args[0]}!")
                return
            
            if not args[1]:
                await ctx.channel.send("Provide a list name: !additem -l <listname>")
                return
            
            # query for a list matching given name
            found: Collection = lkdb.get_collection_by_name(args[1], str(ctx.guild.id))
            if not found:
                await ctx.channel.send(f"No list found with name {args[1]}!")
                return
            Listkeeper.selected_list = found

            # clean args
            args = args[2:]

        ## Create new item
        if Listkeeper.selected_list is None:
            await ctx.channel.send("No list selected! !additem -l <list-name>")
            return

        name: str = args[0]
        note: str = args[1] if args[1] else ""
        new_item: Union[Item, None] = lkdb.create_item(
            name=name,
            note=note,
            item_id=lkdb.generate_id(),
            collection_id=Listkeeper.selected_list.collection_id
        )
        if new_item:
            await ctx.channel.send(f"Successfully created item {new_item.name}")
        else:
            await ctx.channel.send(f"Could not create item!")


            


    ## Read
    @commands.command()
    async def listall(self, ctx) -> None:
        tmp: List[Collection] = lkdb.get_guild_collections(str(ctx.guild.id))
        if tmp:
            collection_names: str = "\n".join([colx.name for colx in tmp])
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

    


    


    
    


    
