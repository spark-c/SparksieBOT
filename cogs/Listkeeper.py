# Cog to keep track of lists made by users
# July 2021
# Collin Sparks

from cogs.listkeeper_db.lkdb import DatabaseError
import discord
from discord.ext import commands
import asyncio
from typing import Union, Dict, List, Optional

from cogs.listkeeper_db.lkdb import Collection, Item
import cogs.listkeeper_db.lkdb as lkdb


class Listkeeper(commands.Cog):
    
    selected_list: Union[Collection, None] = None

    def __init__(self, bot):
        self.bot = bot


    ## Create
    @commands.command()
    async def newlist(self, ctx, *args) -> None:
        name: str = args[0]
        desc: Union[str, None] = None
        if len(args) == 2:
            desc = args[1]

        try:
            new_colx: Collection = lkdb.create_collection(
                name=name,
                description=desc,
                collection_id=lkdb.generate_id(),
                guild_id=str(ctx.guild.id)
            )
            Listkeeper.selected_list = new_colx
            await ctx.channel.send(f"Successfully created {new_colx.name}!")

        except DatabaseError as e:
            await ctx.channel.send(f"Could not create list! Error:\n{e}")
            return


    @commands.command()
    async def additem(self, ctx, *args) -> None:
        ## Check if list name is passed
        if args[0].startswith("-"):
            # handle misuse
            if len(args) > 4:
                await ctx.channel.send("Usage: !additem [-l <listname>] <item-name> [<item-note>]")
                return

            if args[0].lower() not in ["-l", "-list"]:
                await ctx.channel.send(f"Invalid argument: {args[0]}!")
                return
            
            if not args[1]:
                await ctx.channel.send("Provide a list name: !additem -l <listname>")
                return
            
            # query for a list matching given name
            try:
                found: Union[Collection, None] = (
                    lkdb.get_collection_by_name(name=args[1], guild_id=str(ctx.guild.id))
                )
                Listkeeper.selected_list = found
            except DatabaseError as e:
                await ctx.channel.send(f"Could not find list! Error:\n{e}")
                return

            # clean args
            args = args[2:]

        ## Create new item
        if Listkeeper.selected_list is None:
            await ctx.channel.send("No list selected! !additem -l <list-name>")
            return

        name: str = args[0]
        note: Union[str, None] = None
        if len(args) == 2:
            note = args[1]

        try:
            new_item: Item = lkdb.create_item(
                name=name,
                note=note,
                item_id=lkdb.generate_id(),
                collection_id=Listkeeper.selected_list.collection_id
            )
            await ctx.channel.send(f"Successfully created item {new_item.name}")
        except DatabaseError as e:
            await ctx.channel.send(f"Could not create item! Error:\n{e}")
            return


    ## Read
    @commands.command()
    async def listall(self, ctx) -> None:
        try:
            tmp: List[Collection] = lkdb.get_guild_collections(str(ctx.guild.id))
            embed: discord.Embed = create_embed(type='all_collections', all_collections=tmp)
            await ctx.channel.send(embed=embed)
        except DatabaseError as e:
            await ctx.channel.send(f"Nothing found! Error:\n{e}")
            return


    @commands.command()
    async def list(self, ctx, *args) -> None:
        if len(args) > 1:
            await ctx.channel.send("Too many arguments! Use quotes if the list name has spaces.")
            return

        if not args and Listkeeper.selected_list is None:
            await ctx.channel.send("Please supply list name: !list <listname>")
            return

        if (Listkeeper.selected_list) and (not args):
            # refreshes the selected_list; (no args were passed but there is a selected list)
            try:
                updated_colx: Collection = lkdb.get_collection_by_name(
                    name=Listkeeper.selected_list.name,
                    guild_id=str(ctx.guild.id)
                )
                Listkeeper.selected_list = updated_colx
            except DatabaseError as e:
                await ctx.channel.send(f"Attempted to refresh list but could not! Error:\n{e}")

        if args:
            try:
                new_colx: Collection = (
                    lkdb.get_collection_by_name(name=args[0], guild_id=str(ctx.guild.id))
                )
                Listkeeper.selected_list = new_colx
            except DatabaseError as e:
                await ctx.channel.send(f"Could not find list! Error:\n{e}")
                return
        
        # by now, selected_list is the most recent version of whatever list we're using
        if Listkeeper.selected_list is not None:
            embed: discord.Embed = create_embed(type='collection', collection=Listkeeper.selected_list)
            await ctx.channel.send(embed=embed)
        else:
            await ctx.channel.send("Something went wrong! No list was selected.")
        

    ## Update
    @commands.command()
    async def updateitem(self, ctx) -> None:
        pass


    @commands.command()
    async def updatelist(self, ctx) -> None:
        pass


    # Delete
    @commands.command()
    async def rmlist(self, ctx, collection_name) -> None:
        try:
            lkdb.delete_collection_by_name(
                name=collection_name,
                guild_id=str(ctx.guild.id)
            )
            await ctx.channel.send(f"Deleted list {collection_name}!")
        except DatabaseError as e:
            await ctx.channel.send(f"Could not remove list! Error:\n{e}")


    @commands.command()
    async def rmitem(self, ctx, *args) -> None:
        if not (args[0].startswith("-") or Listkeeper.selected_list):
            await ctx.channel.send("No list selected!")
            return

        if args[0].startswith("-"):
            # handle misuse
            if len(args) > 3:
                await ctx.channel.send("Usage: !rmitem [-l <listname>] <item-name>")
                return

            if args[0].lower() not in ["-l", "-list"]:
                await ctx.channel.send(f"Invalid argument: {args[0]}!")
                return
            
            if not args[1]:
                await ctx.channel.send("Provide a list name: !additem [-l <listname>] <item-name>")
                return

            try:
                Listkeeper.selected_list = (
                    lkdb.get_collection_by_name(name=args[1], guild_id=str(ctx.guild.id))
                )
            except DatabaseError as e:
                await ctx.channel.send(f"Couldn't find that list! Error:\n{e}")
            
            # clean args
            args = args[2:]

        if Listkeeper.selected_list is None: # for typechecker
            return
        try:
            lkdb.delete_item(
                collection_name=Listkeeper.selected_list.name,
                guild_id=str(ctx.guild.id),
                item_name=args[0]
            )
            await ctx.channel.send(f"Deleted item '{args[0]}'!")
        except DatabaseError as e:
            await ctx.channel.send(f"Couldn't delete that item! Error:\n{e}")


    # Utility
    @commands.command()
    async def listundo(self, ctx) -> None:
        pass


# ## Helper Functions
def create_embed(
    type: str, 
    *, 
    collection: Optional[Collection] = None, 
    all_collections: Optional[List[Collection]] = None
    ) -> discord.Embed:

    if type not in ['collection', 'all_collections']:
        raise ValueError("Parameter 'type' must be str 'collection' or 'all_collections'")
    
    if type == 'collection' and collection:
        collection_embed: discord.Embed = discord.Embed(
            title=collection.name,
            description=collection.description,
            color=0x109319
        )
        # TODO add logic for handling overflow (>25 fields or 6000 characters)
        for item in collection.items:
            collection_embed.add_field(name=item.name, value=f"> {item.note}", inline=False)
        return collection_embed
    
    if type == 'all_collections' and all_collections:
        all_collections_embed: discord.Embed = discord.Embed(
            title=f"Lists:",
            description="All lists present for this server.",
            color=0x109319
        )
        # TODO add logic for handling overflow (>25 fields or 6000 characters)
        for colx in all_collections:
            all_collections_embed.add_field(name=colx.name, value=f"> {colx.description}", inline=False)
        return all_collections_embed
    
    return discord.Embed(title="Something went wrong!", description="I made it to the end of create_embed() and nothing caught me!")



def setup(bot):
    bot.add_cog(Listkeeper(bot))

    


    


    
    


    
