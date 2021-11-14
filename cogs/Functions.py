# Basic commands for Baby Bot discord bot.
# 8/11/2020
# Collin Sparks

import discord
from discord.ext import commands
import random
import requests
from requests.models import Response
import bs4
from bs4.element import ResultSet
import asyncio
from typing import Dict, List, Tuple
from types import SimpleNamespace


from bot import SparksieBot


class Functions(commands.Cog):

    def __init__(self, bot):
        self.bot: SparksieBot = bot

    @commands.Cog.listener()
    async def on_message(self, ctx) -> None:
        if ctx.content.lower().startswith('good bot'): # Thanks for 'good bot'
            await ctx.channel.send('Thanks!')
        if self.bot.user in ctx.mentions: # Responds to Mentions
            if (ctx.content.lower().startswith('he') or
                ctx.content.lower().startswith('hi')): # hey, hello, hi
                await ctx.channel.send('Hello {0}!'.format(ctx.author))
            else:
                await ctx.channel.send('Beep boop!')


    @commands.command()
    async def ping(self, ctx) -> None:
        await ctx.channel.send('Pong!')


    @commands.command()
    async def marco(self, ctx) -> None: # Replies "Polo!" with a mention of the invoker in a different text channel, if available
        allChannels: List = []
        for channel in ctx.guild.channels:
            if channel.type == discord.ChannelType.text:
                allChannels.append(channel)
        allChannels.remove(ctx.channel)
        if len(allChannels) > 0:
            await allChannels[
                    random.randint(0, len(allChannels) - 1)
                    # TODO: use random.choice instead
                ].send(
                    f"Polo! {ctx.author.mention}"
                ) # make it join a random DIFFERENT channel to say this
        else:
            await ctx.channel.send('Polo!')


    @commands.command()
    async def cat(self, ctx, *terms) -> None: # searches for a random cat picture, or can search optional arguments instead
        # TODO: refactor the 'query' bit of this function to allow for typing
        catQueries: List[str] = ['cat', 'cats', 'happy kitty', 'kitten', 'happy cat', 'cute cat', 'cat in box', 'sleepy cat', 'house cat']
        if terms:
            query = terms
        else:
            # TODO: use random.choice instead
            query = catQueries[random.randint(0, len(catQueries)-1)]

        if query[0] == '-f': # optional arg to return the first search result
            index = 1 # not 0, which will return a google pic from the search page. var is the index of serach result to return
            final_query = query[1:] # removes the '-f' from the search terms
        else:
            final_query = query
            index = random.randint(1,20) # higher ranges risk out-of-index errors

        results: Response = requests.get(
            r'https://google.com/search?q={0}&safe=on&tbm=isch'.format(
                '+'.join(final_query)
            )
        )
        try:
            results.raise_for_status()
        except:
            # TODO: add error handling
            print('ERROR downloading search results')
            await ctx.channel.send('Search Failed! :(')
            return
        parsed: bs4.BeautifulSoup = (
            bs4.BeautifulSoup(results.text, 'html.parser')
        )
        # TODO: figure out the red squiggly .attrs
        images: ResultSet = parsed.select('img')
        imgLink: str = images[index].attrs['src']
        await ctx.channel.send(imgLink)


    @commands.command()
    async def roll(self, ctx, dice:str, *args) -> None:
        """ Generate a random number between min and max, optionally several times. """
        # TODO: seed should be indicated with a FLAG, not as positional argument
        try:
            temp_strings: List[str] = dice.split("d") # "4d6" = ["4", "6"]
            nums: List[int] = list(map(
                lambda s: int(s), temp_strings
            ))
            for num in nums:
                if num < 1:
                    await ctx.channel.send("Values must be greater than zero!")
                    return

            iters: int = nums[0]
            die_size: int = nums[1]
        except:
            await ctx.channel.send("Usage: !roll 4d6")
            return

        rolls: List[int] = list()
        for _ in range(iters): # generate the numbers
            if "--test" in args:
                random.seed(24601)
            rolls.append(random.randint(1, die_size))

        results: List[str] = list(map(lambda n: str(n), rolls))
        message: str = (
            "Here are your numbers: " +
            ", ".join(results) + 
            f"\n Sum: {sum(rolls)}"
        )
        await ctx.channel.send(message)

        # TODO: continue type-checking below here


    @commands.command()
    async def teampicker(self, ctx, sharks:int, jets:int) -> None: #team1size vs team2size
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
    async def say(self, ctx, *args:str) -> None:
        if str(ctx.message.author) == 'spark.c#7001':
            await ctx.message.delete()
            await ctx.channel.send(' '.join(args))
        else:
            await ctx.channel.send('Nice try. I\'m not your mouthpiece anymore!')


    @commands.command()
    async def sleepy(self, ctx) -> None:
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
    async def lotr(self, ctx, *args) -> None: #grabs a random quote from source site
        attempts: int = 0
        while attempts < 3:
            if "--test" in args:
                print("TESTING!!!")
                # always generates queryIndex==34
                random.seed(24601)
            queryIndex: int = random.randint(1, 64) # 64 quotes on the site
            queryURL: str = f"http://lotrproject.com/quotes/quote/{str(queryIndex)}"
            headers: Dict[str, str] = {
                'User-Agent':
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0"
            } # site rejects plain python requests
            results: Response = requests.get(queryURL, headers=headers)

            try:
                results.raise_for_status()
                break
            except Exception as e:
                print(e)
                attempts += 1
                continue
        else:
            await ctx.channel.send("I couldn't find a quote!")
            return

        try:
            parsed: bs4.BeautifulSoup = bs4.BeautifulSoup(
                results.text, 'html.parser'
            )
            quote = parsed.find(class_ = 'text')
            character = parsed.find(class_ = 'character')
            source = parsed.find(class_ = 'source')
        except:
            await ctx.channel.send("Something went wrong!")
            return

        if quote is None:
            quote = SimpleNamespace(**{"text": "<quote not found>"})
        if character is None:
            character = SimpleNamespace(**{"text": "<speaker unknown>"})
        if source is None:
            source = SimpleNamespace(**{"text": "<source unknown>"})

        quoteEmbed: discord.Embed = discord.Embed(name='', description=quote.text)
        quoteEmbed.add_field(name=character.text, value=source.text)

        await ctx.channel.send(embed=quoteEmbed)


    @commands.command()
    async def help_printout(self, ctx) -> None:
	    await ctx.channel.send(r'''
.
!cat - returns a random cat picture! you can type something after '!cat' to search for that query instead of cat.

!marco - pings you with 'Polo!' from a different text channel.

!ping - Pong!

!roll - usage: !roll 4d6

!say - makes the bot say whatever you type after !say (sparksie only)

!sleepy - turns bot off (confirm with a reply of 'y')

!teampicker - usage: !teampicker (team1size) (team2size) // returns numbers in the format [ 1, 2 ] vs [ 3, 4, 5 ] in random order to assign teams. Plans to optionally use names from an occupied voice channel instead.

!help - lists available commands

!help (command) - shows usage of given command

!help_printout - shows this message.''')


def setup(bot):
    bot.add_cog(Functions(bot))
