# Cog to keep track of lists made by users
# July 2021
# Collin Sparks

from cogs.listkeeper_db.lkdb import DatabaseError
import discord
from discord.ext import commands
import asyncio
from typing import Union, Dict, List, Optional
from argparse import Namespace # for type annots

from cogs.listkeeper_db.lkdb import Collection, Item
import cogs.listkeeper_db.lkdb as lkdb
import cmdparser


class Listkeeper(commands.Cog):
    
    selected_list: Dict[str,Collection] = dict() # str key is str(guild_id)

    def __init__(self, bot):
        self.bot = bot


    ## Create
    @commands.command()
    async def newlist(self, ctx, *args) -> None:
        try:
            pargs: Namespace = cmdparser.newlist.parse_args(args)
        except cmdparser.ArgumentError as e:
            await self.handle_argument_error(ctx, e)
            return

        name: str = pargs.list_name
        desc: Union[str, None] = pargs.list_description

        try:
            new_colx: Collection = lkdb.create_collection(
                name=name,
                description=desc,
                collection_id=lkdb.generate_id(),
                guild_id=str(ctx.guild.id)
            )
            Listkeeper.selected_list[str(ctx.guild.id)] = new_colx
            await ctx.channel.send(f"Successfully created {new_colx.name}!")

        except DatabaseError as e:
            await ctx.channel.send(f"Could not create list! Error:\n{e}")
            return


    @commands.command()
    async def additem(self, ctx, *args) -> None:
        try:
            pargs: Namespace = cmdparser.additem.parse_args(args)
        except cmdparser.ArgumentError as e:
            await self.handle_argument_error(ctx, e)
            return

        ## Check if list name is passed
        if pargs.l is not None:
            # query for a list matching given name
            try:
                found: Union[Collection, None] = (
                    lkdb.get_collection_by_name(name=pargs.l, guild_id=str(ctx.guild.id))
                )
                Listkeeper.selected_list[str(ctx.guild.id)] = found
            except DatabaseError as e:
                await ctx.channel.send(f"Could not find list! Error:\n{e}")
                return

        if str(ctx.guild.id) not in Listkeeper.selected_list:
            await ctx.channel.send("No list selected! !additem -l <list-name>")
            return

        try:
            new_item: Item = lkdb.create_item(
                name=pargs.item_name,
                note=pargs.item_description,
                item_id=lkdb.generate_id(),
                collection_id=Listkeeper.selected_list[str(ctx.guild.id)].collection_id
            )
            await ctx.channel.send(f"Successfully created item {new_item.name}")
        except DatabaseError as e:
            await ctx.channel.send(f"Could not create item! Error:\n{e}")
            return


    ## Read
    @commands.command()
    async def listall(self, ctx) -> None:
        # TODO Add # of items in each collection
        try:
            tmp: List[Collection] = lkdb.get_guild_collections(str(ctx.guild.id))
            embed: discord.Embed = create_embed(type='all_collections', all_collections=tmp)
            await ctx.channel.send(embed=embed)
        except DatabaseError as e:
            await ctx.channel.send(f"Nothing found! Error:\n{e}")
            return


    @commands.command()
    async def list(self, ctx, *args) -> None:
        try:
            pargs: Namespace = cmdparser.list.parse_args(args)
        except cmdparser.ArgumentError as e:
            await self.handle_argument_error(ctx, e)
            return

        if pargs.list_name is None:
            if str(ctx.guild.id) not in Listkeeper.selected_list:
                await ctx.channel.send("Please supply list name: !list <listname>")
                return

            elif str(ctx.guild.id) in Listkeeper.selected_list:
                # refreshes the selected_list; (no args were passed but there is a selected list)
                try:
                    updated_colx: Collection = lkdb.get_collection_by_name(
                        name=Listkeeper.selected_list[str(ctx.guild.id)].name,
                        guild_id=str(ctx.guild.id)
                    )
                    Listkeeper.selected_list[str(ctx.guild.id)] = updated_colx
                except DatabaseError as e:
                    await ctx.channel.send(f"Attempted to refresh list but could not! Error:\n{e}")
                    return

        elif pargs.list_name is not None:
            try:
                new_colx: Collection = (
                    lkdb.get_collection_by_name(name=args[0], guild_id=str(ctx.guild.id))
                )
                Listkeeper.selected_list[str(ctx.guild.id)] = new_colx
            except DatabaseError as e:
                await ctx.channel.send(f"Could not find list! Error:\n{e}")
                return
        
        # by now, selected_list is the most recent version of whatever list we're using
        if str(ctx.guild.id) in Listkeeper.selected_list:
            embed: discord.Embed = create_embed(
                type='collection', 
                collection=Listkeeper.selected_list[str(ctx.guild.id)]
                )
            await ctx.channel.send(embed=embed)
            return
        else:
            await ctx.channel.send("Something went wrong! No list was selected.")
            return
        

    ## Update
    @commands.command()
    async def updatelist(self, ctx, *args) -> None:
        pass


    @commands.command()
    async def updateitem(self, ctx, *args) -> None:
        pass


    # Delete
    @commands.command()
    async def rmlist(self, ctx, *args) -> None:
        try:
            pargs: Namespace = cmdparser.rmlist.parse_args(args)
        except cmdparser.ArgumentError as e:
            await self.handle_argument_error(ctx, e)
            return

        try:
            lkdb.delete_collection_by_name(
                name=pargs.list_name,
                guild_id=str(ctx.guild.id)
            )
            await ctx.channel.send(f"Deleted list {pargs.list_name}!")
        except DatabaseError as e:
            await ctx.channel.send(f"Could not remove list! Error:\n{e}")


    @commands.command()
    async def rmitem(self, ctx, *args) -> None:
        try:
            pargs: Namespace = cmdparser.rmitem.parse_args(args)
        except cmdparser.ArgumentError as e:
            await self.handle_argument_error(ctx, e)
            return

        if pargs.l is None:
            if str(ctx.guild.id) not in Listkeeper.selected_list:
                await ctx.channel.send("No list selected!")
                return
            
        if pargs.l is not None:
            try:
                Listkeeper.selected_list[str(ctx.guild.id)] = (
                    lkdb.get_collection_by_name(name=args[1], guild_id=str(ctx.guild.id))
                )
            except DatabaseError as e:
                await ctx.channel.send(f"Couldn't find that list! Error:\n{e}")

        if str(ctx.guild.id) not in Listkeeper.selected_list: # for typechecker
            return

        try:
            lkdb.delete_item(
                collection_name=Listkeeper.selected_list[str(ctx.guild.id)].name,
                guild_id=str(ctx.guild.id),
                item_name=pargs.item_name
            )
            await ctx.channel.send(f"Deleted item '{pargs.item_name}'!")
        except DatabaseError as e:
            await ctx.channel.send(f"Couldn't delete that item! Error:\n{e}")


    # Utility
    @commands.command()
    async def listundo(self, ctx) -> None:
        pass


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

    


    


    
    


    
