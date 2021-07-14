# Cog to keep track of lists made by users
# July 2021
# Collin Sparks

from cogs.listkeeper_db.lkdb import DatabaseError
import discord
from discord.ext import commands
import asyncio
from typing import Union, Dict, List, Optional

from sqlalchemy.sql.expression import select

try:
    from cogs.listkeeper_db.lkdb import Collection, Item
    import cogs.listkeeper_db.lkdb as lkdb
except ImportError as e:
    print(e)
    raise ImportError(e)


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

        new_colx: Union[Collection, None] = lkdb.create_collection(
            name=name,
            description=desc,
            collection_id=lkdb.generate_id(),
            guild_id=str(ctx.guild.id)
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
            found: Union[Collection, None] = (
                lkdb.get_collection_by_name(name=args[1], guild_id=str(ctx.guild.id))
            )
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
        note: Union[str, None] = None
        if len(args) == 2:
            note = args[1]

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
            embed: discord.Embed = create_embed(type='all_collections', all_collections=tmp)
            await ctx.channel.send(embed=embed)
        else:
            await ctx.channel.send("No lists found!")


    @commands.command()
    async def list(self, ctx, *args) -> None:
        if len(args) > 1:
            await ctx.channel.send("Too many arguments! Use quotes if the list name has spaces.")
            return

        if not args and Listkeeper.selected_list is None:
            await ctx.channel.send("Please supply list name: !list <listname>")
            return

        if args:
            new_colx: Union[Collection, None] = (
                lkdb.get_collection_by_name(name=args[0], guild_id=str(ctx.guild.id))
            )
            if new_colx:
                Listkeeper.selected_list = new_colx
            else:
                await ctx.channel.send(f"No list found by name {args[0]}!")
                return
        # refreshes the selected_list; (no args were passed but there is a selected list)
        elif Listkeeper.selected_list is not None: # condition present to satisfy type annots
            try:
                updated_colx: Union[Collection, None] = lkdb.get_collection_by_name(
                    name=Listkeeper.selected_list.name,
                    guild_id=str(ctx.guild.id)
                )
                Listkeeper.selected_list = updated_colx
            except :
                await ctx.channel.send(f"Attempted to refresh list but could not!")
        
        # by now, selected_list is the most recent version of whatever list we're using
        if Listkeeper.selected_list is not None:
            embed: discord.Embed = create_embed(type='collection', collection=Listkeeper.selected_list)
            await ctx.channel.send(embed=embed)
        else:
            await ctx.channel.send("Something went wrong!")
        

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


# ## Helper Functions
def create_embed(type: str, *, collection: Optional[Collection] = None, all_collections: Optional[List[Collection]] = None) -> discord.Embed:
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

    


    


    
    


    
