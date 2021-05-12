# Cog to keep track of lists made by users

import discord
from discord.ext import commands
import asyncio
import os
import json


class Collection():

    master = []

    def __init__(self, name, desc):
        self.name = name
        self.desc = desc
        self.contents = []


    def delete(self):
        print(f'Removing {self.name} from Listkeeper!')
        Collection.master.remove(self)


    def add_item(self, label, note): #
        item = {
            'label': label,
            'note': note
        }
        self.contents.append(item)
        save_to_file()


def read_from_file():
    pass


def save_to_file():
    pass


class ListKeeper(commands.cog):

    def __init__(self, bot):
        self.bot = bot


    def dir_init(self, ctx):
        # check for directory exists
        # if os.path.isdir(str(ctx.message.guild.id)):
        #   ctx.channel.send('All set up!')
        # else:
        #   ctx.channel.send('Setting up folder!')
        #   make folder
        pass


    @commands.command()
    def list(self, ctx, colx_name=None):
        # if not colx_name: return [self.name for name in Collection.master]
        # else: 1)Find where Collection.master.name == colx_name and return that obj; 2)Return that obj info
        pass