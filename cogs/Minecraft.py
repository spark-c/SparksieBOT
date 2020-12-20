# Minecraft Server query commands for Baby Bot discord bot.
# 12/20/2020
# Collin Sparks

import discord
from discord.ext import commands
import asyncio
import mcstatus

blueServer = {'host': 'ca2.villagerhost.net',
            'port': 25601 }

class Minecraft(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def playercount(self, ctx, getNames=None): #getNames is an optional arguement to return the list of playernames
        
        await ctx.channel.send(buildQueryReturn(queryServer(), getNames))


            
def writeError(failstep):
    errormsg = ('Server {} failed :(\n'.format(failstep) +
            '<@259610120294498304> fix your shit!'.format('')) #this is my discord user ID
    return errormsg


def queryServer():
    errorcode = 0
    result = None
    try:
        server = mcstatus.MinecraftServer(blueServer['host'], blueServer['port'])
    except:
        errorcode = 1
        result = writeError('lookup')
        return (errorcode, result) #if something goes wrong, queryTuple[1] is the error message
        
    try:
        query = server.query()
    except:
        errorcode = 1
        result = writeError('query')
        return (errorcode, result)

    return (errorcode, query) #if everything works, then queryTuple[1] is the query object

def buildQueryReturn(queryTuple, getNames):
    if queryTuple[0] == 1: #something went wrong
        return queryTuple[1] #the error message
    else:
        playernames = queryTuple[1].players.names #queryTuple[1] is the query object
        playercount = len(playernames)
        message = 'There are currently {} players connected to the Baby Blue Minecraft server'.format(playercount)
        if getNames == 'names': #optional argument 'names' from the original command
            message = message + "\n\nHere are the connected players:\n{}".format('\n'.join(playernames))

        return message



        

def setup(bot):
    bot.add_cog(Minecraft(bot))


    
