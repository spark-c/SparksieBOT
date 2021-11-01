import discord
import logging
from discord.ext import commands
import random
import asyncio
import os
import datetime as dt
from typing import Union

from discord.ext.commands.bot import Bot

import utils.groovycommands as groovycommands

logger: logging.Logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler: logging.FileHandler = logging.FileHandler(
    filename='discord.log',
    encoding='utf-8',
    mode='w'
    )
handler.setFormatter(
    logging.Formatter(
        '%(asctime)s:%(levelname)s:%(name)s: %(message)s'
        )
    )
logger.addHandler(handler)

# Tiny subclass to add a property used for "pausing" the bot
class SparksieBot(commands.Bot):
    def __init__(
        self,
        command_prefix='!',
        intents=discord.Intents.default(),
        loop=None
        ):
        super().__init__(
            command_prefix=command_prefix,
            intents=intents,
            loop=loop
        )
        self.paused_guilds = set()

    async def process_commands(self, message):
        """ overriding this to allow receiving commands from WidgetBot """
        if message.author.bot:
            if message.author.id != 871218166540427324: # WidgetBot id
                return

        ctx = await self.get_context(message)
        await self.invoke(ctx)

intents = discord.Intents.default()
intents.members = True
intents.typing = False
intents.presences = False
bot: SparksieBot = SparksieBot(command_prefix='!', intents=intents)

last_glory: dt.datetime = dt.datetime.now() - dt.timedelta(seconds=120)

@bot.event
async def on_ready() -> None:
    print('Logged in as {0.user}!'.format(bot))

@bot.event
async def on_message(message) -> None:
    global last_glory

    if message.author == bot.user:
        return

    # if someone says glory (with cooldown timer)
    if ('glory' in message.content.lower() and
        (dt.datetime.now() - last_glory).seconds > 120):
        last_glory = dt.datetime.now()
        await message.channel.send("Glory!")

    #if the message is a groovy command
    if (message.content.lower().startswith('-') and
    message.channel.name != 'groovybot-corner'):
        for command in groovycommands.groovycommands:
            if message.content.lower().startswith(command):
                await message.delete()
                await message.channel.send(
                    'No littering. Keep the trash in the correct channel.'
                )

                targetChannel: Union[discord.TextChannel, None] = (
                    discord.utils.get(
                        message.guild.text_channels,
                        name='groovybot-corner'
                    )
                )
                if targetChannel is not None:
                    await targetChannel.send(
                        f"{message.author.mention} Where it belongs."
                    )

    #Checks if the message was sent by Groovy / in the wrong channel
    if (str(message.author) == 'Groovy#7254' and
    message.channel.name != 'groovybot-corner'): 
        await message.delete()

    if 'groovy' in message.content.lower():
        await message.channel.send('...')

    if 'congrat' in message.content.lower():
        for i in range(0,2):
            await message.channel.send(
                ':confetti_ball::confetti_ball::confetti_ball:\nCONGRATULATIONS!!!'
            )

    if message.channel.name == 'arma-discussion':
        counter: int = random.randint(1,100)
        if counter < 3:
            await message.channel.send('USAF is still watching.')

    try:
        if message.content.startswith("!unpause"):
            await bot.process_commands(message)
        elif str(message.guild.id) not in bot.paused_guilds:
            await bot.process_commands(message) #this is required or the bot will be stuck in the on_message and not see the commands
        else:
            await message.add_reaction("⏸️") # a pause symbol
    except:
        return


@bot.command()
async def pause(ctx) -> None:
    bot.paused_guilds.add(str(ctx.guild.id))
    await ctx.channel.send("Paused!")


@bot.command()
async def unpause(ctx) -> None:
    try:
        bot.paused_guilds.remove(str(ctx.guild.id))
        await ctx.channel.send("Unpaused!")
    except KeyError:
        await ctx.channel.send("Can't unpause; nothing was paused!")


@bot.command()
async def load(ctx, extension) -> None:
    await my_load(ctx, extension, bot)


@bot.command()
async def unload(ctx, extension) -> None:
    await my_unload(ctx, extension, bot)


@bot.command()
async def reload(ctx, extension) -> None:
    await my_unload(ctx, extension, bot)
    await my_load(ctx, extension, bot)


async def my_load(ctx, extension, bot) -> None:
    try:
        bot.load_extension('cogs.{0}'.format(extension))
        await ctx.channel.send('Extension \'{0}\' loaded!'.format(extension))
    except:
        await ctx.channel.send('Load \'{0}\' failed!'.format(extension))


async def my_unload(ctx, extension, bot) -> None:
    try:
        bot.unload_extension('cogs.{0}'.format(extension))
        await ctx.channel.send('Extension \'{0}\' unloaded!'.format(extension))
    except:
        await ctx.channel.send('Unload \'{0}\' failed!'.format(extension))


print('working directory is {0}'.format(os.getcwd()))

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        try:
            loadThis: str = filename[:-3]
            bot.load_extension('cogs.{0}'.format(loadThis))
            print('cog ' + filename + ' loaded.')
        except Exception as e:
            print('cog ' + filename + ' failed!')
            print(e)

#For use when running from a real filesystem
try:
    with open(r'./baby-bot-token.txt', 'r') as f:
        token: str = f.read()
    bot.run(token)
except: #For use when deployed via heroku (using config vars to feed in the token)
    bot.run(os.environ["TOKEN"])
