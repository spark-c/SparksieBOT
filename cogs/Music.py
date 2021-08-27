# Music playing commands for SparksieBOT
# 08/26/2021
# Collin Sparks

# IMPORTANT!
# The use of this cog requires FFMPEG.
# On Heroku, we'll need to ensure we use two buildpacks:
# 1. heroku/python
# 2. https://github.com/jonathanong/heroku-buildpack-ffmpeg-latest.git
#
# REFERENCE: https://stackoverflow.com/questions/58146519/how-to-use-the-heroku-buildpack-ffmpeg-for-python

import discord # we will be using discord.FFmpegPCMAudio
from discord.ext import commands
from pytube import YouTube
from typing import Union

from baby_bot import SparksieBot


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot: SparksieBot = bot

    @commands.command()
    async def play(self, ctx, *args) -> None:
        await ctx.channel.send("play command invoked!")




def setup(bot):
    bot.add_cog(Music(bot))