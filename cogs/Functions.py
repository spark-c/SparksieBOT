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

    @commands.Cog.listener()
    async def on_message(self, ctx):
        if ctx.content.lower().startswith('good bot'): # Thanks for 'good bot'
            await ctx.channel.send('Thanks!')
        if self.bot.user in ctx.mentions: # Responds to Mentions
            print(ctx.content)
            if ctx.content.lower().startswith('he') or ctx.content.lower().startswith('hi'): # hey, hello, hi
                await ctx.channel.send('Hello {0}!'.format(ctx.author))
            else:
                await ctx.channel.send('Beep boop!')


    @commands.command()
    async def ping(self, ctx):
        await ctx.channel.send('Pong!')

    @commands.command()
    async def marco(self, ctx): # Replies "Polo!" with a mention of the invoker in a different text channel, if available
        allChannels = []
        for channel in ctx.guild.channels:
            if channel.type == discord.ChannelType.text:
                allChannels.append(channel)
        allChannels.remove(ctx.channel)
        if len(allChannels) > 0:
            await allChannels[random.randint(0, len(allChannels) - 1)].send('Polo! {0}'.format(ctx.author.mention)) # make it join a random DIFFERENT channel to say this
        else:
            await ctx.channel.send('Polo!')

    @commands.command()
    async def cat(self, ctx, *terms): # searches for a random cat picture, or can search optional arguments instead
        catQueries = ['cat', 'cats', 'happy kitty', 'kitten', 'happy cat', 'cute cat', 'cat in box', 'sleepy cat', 'house cat']
        if terms:
            query = terms
        else:
            query = catQueries[random.randint(0, len(catQueries)-1)]
        results = requests.get(r'https://google.com/search?q={0}&safe=on&tbm=isch'.format('+'.join(query)))
        try:
            results.raise_for_status()
        except:
            print('ERROR downloading search results')
            await ctx.channel.send('Search Failed! :(')
            return
        parsed = bs4.BeautifulSoup(results.text, 'html.parser')
        images = parsed.select('img')
        index = random.randint(1,20) # higher ranges result in out-of-index errors
        imgLink = images[index].attrs['src']
        await ctx.channel.send(imgLink)

    @commands.command()
    async def roll(self, ctx, dice:str): #generate a random number between min and max, optionally several times.
        try:
            dice = dice.split('d') # 4d6 = [4, 6]
            for i in range(0, len(dice)):
                dice[i] = int(dice[i])
                iters = dice[0]
        except:
            await ctx.channel.send('Usage: !roll 4d6')

        ints = []
        temp = []
        for i in range(0, iters): #generate the numbers
            ints.append(random.randint(1, dice[1])) # number between 1 and size of die (includes endpoint)
        for i in range(0, len(ints)): #turn them into str for printing
            temp.append(str(ints[i]))
        result = 'Here are your numbers: ' + ', '.join(temp) + '\n Sum: {}'.format(sum(ints))
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
        if str(ctx.message.author) == 'spark.c#7001':
            await ctx.message.delete()
            await ctx.channel.send(' '.join(args))
        else:
            await ctx.channel.send('Nice try. I\'m not your mouthpiece anymore!')

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

    @commands.command()
    async def help_printout(self, ctx):
	    await ctx.channel.send(r'''
.
!cat - returns a random cat picture! you can type something after '!cat' to search for that query instead of cat.

!marco - pings you with 'Polo!' from a different text channel.

!ping - Pong!

!roll - usage: !roll 4d6

!say - makes the bot say whatever you type after !say

!sleepy - turns bot off (confirm with a reply of 'y')

!teampicker - usage: !teampicker (team1size) (team2size) // returns numbers in the format [ 1, 2 ] vs [ 3, 4, 5 ] in random order to assign teams. Plans to optionally use names from an occupied voice channel instead.

!help - lists available commands

!help (command) - shows usage of given command

!help_printout - shows this message.''')


def setup(bot):
    bot.add_cog(Functions(bot))
