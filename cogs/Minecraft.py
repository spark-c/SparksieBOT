# Minecraft Server query commands for Baby Bot discord bot.
# 12/20/2020
# Collin Sparks

import discord
from discord.ext import commands
import asyncio
from mcstatus
            

class Minecraft(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def playercount(self, ctx, getList=False):
        
        await ctx.channel.send(buildQueryReturn(queryServer(), getList))


            
def writeError(failstep)
    errormsg = 'Server {} failed :(\n'.format(failstep) +
            '@{} fix your shit!'.format('259610120294498304')) #this is my discord user ID
    return errormsg


def queryServer():
    errorcode = 0
    try:
        server = mcstatus.MinecraftServer('ca2.villagerhost.net',25601)
    except:
        errorcode = 1
        result = writeError('lookup')
        
    try:
        query = server.query()
    except:
        errorcode = 1
        result = writeError('query')

    return (errorcode, result)

def buildQueryReturn(queryTuple, getList):
    if queryTuple[0] = 1: #something went wrong
        return queryTuple[1] #the error message
    else:
        playerlist = query.players.names
        playercount = len(playerlist)
        message = 'There are currently {} players connected to the Baby Blue Minecraft server'.format(playercount)AssertionError
        if getList == 'list':
            message = message + "\n\nHere are the connected players:\n{}".format('\n'.join(playerlist))

        return message



        



    
