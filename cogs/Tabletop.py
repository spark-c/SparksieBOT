#Cog with functions relating to organizing Board Game Nights.
#Collin Sparks, created 2/20/2021
#Python 3

import discord
from discord.ext import commands
import asyncio
import os
import json


class Game(): # ideally we'd always specify the playercount, but let's be real.

    games = read_games() # a list of objects
    games_message = generate_gamelist()

    def __init__(self, name, players, note):
        self.name = name
        self.players = players
        self.note = note
        self.printout = {self.name: "({} players)".format(self.players)} # "Battleship (2 players)". is a dict for sorting by players later


def get_key(element): # for the generate_gamelist function sorting by dict values
    return element.get


def read_games(): # reads existing data from .json file in parent directory
    games = []
    if not os.path.isfile('../tabletop.json'):
        with open('../tabletop.json', 'a') as f: # append mode; not writing anything though, it will just create if doesn't exist
            print('created new tabltop.json file')
            return []
    else:
        try:
            with open('../tabletop.json', 'r') as f:
                found_data = json.load(f)
            for instance in found_data:
                instance = Game(instance['name'], instance['players'], instance['note']) # inits instances of objs from data
            games.append(instance)
            return games
        except:
            print('ERROR LOADING TABLETOP.json')
            return []


def generate_gamelist(sort=None): # returns message to be delivered by the bot
    message = ["Games we're looking at:"]
    working = []
    for game in Game.games:
        working.append(game)
        if sort: # user indicated a sort method
            if sort == 'players-low':
                working = sorted(working, key=get_key) # should sort by each dict's value [{name1: 1}, {name2: 2}, ...]
            elif sort == 'players-high':
                working = sorted(working, reverse=True, key=get_key)
    for game in working: #this is now a sorted list of dicts
        for i, j in game.items(): #unpacks dict key and value into one string
            gamestring = i + ': ' + "{} players".format(j) # "key: value players"
            message.append(gamestring)

    return message



class Tabletop(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def gamelist(self, ctx, sort=None, utility=None): # prints list of games; optional sort by playercount
        if sort: #if user requested a sort method
            message = generate_gamelist(sort)
        else:
            message = Game.games_message

        await ctx.channel.send(message)

    @commands.command()
    async def add_game(self, ctx, name, players=3, note=''):
        try:
            addthis = Game(name, players, note)
            Game.games.append(addthis)
            await ctx.channel.send('Successfully added {}!'.format(name))
        except:
            await ctx.channel.send('Something went wrong!')

    @commands.command()
    async def delete_game(self, ctx, name):
        pass
