# Basic commands for Baby Bot discord bot.
# 8/11/2020
# Collin Sparks

import discord
from discord.ext import commands
import random
import requests
import bs4
import asyncio

class Functions(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    # @commands.Cog.listener()
    # async def on_message(self):
    #     pass

    @commands.command()
    async def ping(self, ctx):
        await ctx.channel.send('Pong!')

    @commands.command()
    async def marco(self, ctx):
        await ctx.channel.send('Polo!') # make it join a DIFFERENT channel to say this

    @commands.command()
    async def cat(self, ctx):
        catQueries = ['cat', 'cats', 'happy+kitty', 'kitten', 'happy+cat', 'cute+cat', 'cat+in+box', 'sleepy+cat', 'house+cat']
        query = catQueries[random.randint(0, len(catQueries)-1)]
        print('searching for {0}'.format(query))
        results = requests.get(r'https://google.com/search?q={0}&safe=on&tbm=isch'.format(query))
        try:
            results.raise_for_status()
        except:
            print('ERROR downloading search results')
            await ctx.channel.send('Search Failed! :(')
            return
        parsed = bs4.BeautifulSoup(results.text, 'html.parser')
        images = parsed.select('img')
        index = random.randint(1,20)
        print('index is {0}'.format(index))
        imgLink = images[index].attrs['src']
        await ctx.channel.send(imgLink)

    @commands.command()
    async def rng(self, ctx, min:int, max:int, iters:int=1): #generate a random number between min and max, optionally several times.
        ints = []
        temp = []
        for i in range(0, iters): #generate the numbers
            ints.append(random.randint(min, max))
        for i in range(0, len(ints)): #turn them into str for printing
            temp.append(str(ints[i]))
        result = 'Here are your numbers: ' + ', '.join(temp)
        await ctx.channel.send(result)

    @commands.command()
    async def teampicker(self, ctx, sharks:int, jets:int): #team1size vs team2size
        lineup = []
        for i in range(0, sharks + jets): #creates list to pick from
            lineup.append(i + 1) # +1 so that we get regular counting numbers
        random.shuffle(lineup)
        teamOne = lineup[:sharks]
        teamTwo = lineup[sharks:]
        await ctx.channel.send('Here\'s the lineup:\n{0} vs. {1}'.format(teamOne, teamTwo))
        await asyncio.sleep(3)
        await ctx.channel.send('noobs')
    
    @commands.command()
    async def say(self, ctx, *args:str):
        await ctx.message.delete()
        await ctx.channel.send(' '.join(args))

    @commands.command()
    async def hello(self, ctx, arg):
        await ctx.send(arg)

    @commands.command()
    async def sleepy(self, ctx):
        await ctx.channel.send('Is it my bedtime? (y/n)')

        try:
            msg = await self.bot.wait_for('message', timeout = 5.0, check=lambda message: message.author == ctx.author)
        except:
            await ctx.channel.send("I'm not tired yet!")
            return
        if msg.content.lower().startswith('y'):
            await ctx.channel.send('Good night, sweet prince.')
            await self.bot.close()
        else:
            await ctx.channel.send("I'm not tired yet!")


def setup(bot):
    bot.add_cog(Functions(bot))