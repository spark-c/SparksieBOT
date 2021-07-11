# Cog to keep track of lists made by users

import discord
from discord.ext import commands
import asyncio
from typing import Union, Dict, List

import listkeeper_db.lkdb as lkdb


class Listkeeper(commands.cog):
    

    ## Create
    @commands.command
    def newlist(ctx) -> None:
        pass


    @commands.command
    def additem(ctx) -> None:
        pass


    ## Read
    @commands.command
    def listall(ctx) -> None:
        pass


    @commands.command
    def list(ctx) -> None:
        pass


    ## Update
    @commands.command
    def updateitem(ctx) -> None:
        pass


    @commands.command
    def updatelist(ctx) -> None:
        pass


    # Delete
    @commands.command
    def rmlist(ctx) -> None:
        pass


    @commands.command
    def rmitem(ctx) -> None:
        pass


    # Utility
    @commands.command
    def listundo(ctx) -> None:
        pass




    


    


    
    


    
