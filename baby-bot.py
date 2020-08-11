import discord
import logging
from discord.ext import commands
import asyncio
import random

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print('Logged in as {0.user}!'.format(bot))

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if message.content.lower().startswith('congrat'):
        for i in range(0,2):
            await message.channel.send(':confetti_ball::confetti_ball::confetti_ball:\nCONGRATULATIONS!!!')
    
    if message.channel.name == 'arma-discussion':
        counter = random.randint(1,100)
        if counter < 3:
            await message.channel.send('USAF is watching.')

    try:
        await bot.process_commands(message) #this is required or the bot will be stuck in the on_message and not see the commands
    except:
        return


@bot.command()
async def rng(ctx, min:int, max:int, iters:int=1): #generate a random number between min and max, optionally several times.
    ints = []
    temp = []
    for i in range(0, iters): #generate the numbers
        ints.append(random.randint(min, max))
    for i in range(0, len(ints)): #turn them into str for printing
        temp.append(str(ints[i]))
    result = 'Here are your numbers: ' + ', '.join(temp)
    await ctx.channel.send(result)

@bot.command()
async def teampicker(ctx, sharks:int, jets:int): #team1size vs team2size
    lineup = []
    for i in range(0, sharks + jets): #creates list to pick from
        lineup.append(i + 1) # +1 so that we get regular counting numbers
    random.shuffle(lineup)
    teamOne = lineup[:sharks]
    teamTwo = lineup[sharks:]
    await ctx.channel.send('Here\'s the lineup:\n{0} vs. {1}'.format(teamOne, teamTwo))
    await asyncio.sleep(3)
    await ctx.channel.send('noobs')

@bot.group(pass_context=True)
async def event():
    pass

@event.command()
async def propose(ctx, name:str, day:str, time:str):
    pass

@event.command()
async def cancel(ctx, name:str):
    pass

@event.command(name='list')
async def _list(ctx):
    pass

@bot.command()
async def music():
    pass

@bot.command()
async def say(ctx, *args:str):
    await ctx.message.delete()
    await ctx.channel.send(' '.join(args))

@bot.command()
async def hello(ctx, arg):
    await ctx.send(arg)

@bot.command()
async def sleepy(ctx):
    await ctx.channel.send('Good night, sweet prince.')
    await bot.close()

with open(r'./baby-bot-token.txt', 'r') as f:
    token = f.read()
bot.run(token)
