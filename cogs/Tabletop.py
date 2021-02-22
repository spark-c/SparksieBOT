#Cog with functions relating to organizing Board Game Nights.
#Collin Sparks, created 2/20/2021
#Python 3

import discord
from discord.ext import commands
import asyncio
import os
import json


class Game(): # ideally we'd always specify the playercount, but let's be real.

    games = [] # a list of objects
    games_message = None # this will start as None, but will be updated upon the first call of generate_gamelist()

    def __init__(self, name, players='3', note=''):
        self.name = name
        self.players = str(players) # str() for the sake of ease while using the shell
        self.note = note
        self.printout = {self.name: "({} players)".format(self.players)} # "Battleship (2 players)". is a dict for sorting by players later

        Game.games.append(self)


def read_games(): # reads existing data from .json file in parent directory
    try:
        with open('./tabletop.json', 'r') as f:
            json_data = json.loads(json.load(f))
        for instance in json_data:
            instance = Game(instance['name'], instance['players'], instance['note']) # inits instances of objs from data
    except:
        print('Couldn\'t load tabletop.json!')


def save_games():
    outfile = './tabletop.json'
    json_string = json.dumps([obj.__dict__ for obj in Game.games], indent=4)
    print('JSON STRING:' + json_string)
    try:
        with open(outfile, 'w') as f:
            json.dump(json_string, f) # dict form of that object, or else we get error 'not JSON serializable'
    except:
        print('ERROR saving gameslist to file!')



def sort_by(element):
    return int(element.players)


def to_final_string(message): # turns list of strings into one string for delivery to users
    joined_message = '\n'.join(message)
    return joined_message


def generate_gamelist(sort=None): # returns message to be delivered by the bot
    message = ["Games we're looking at:"]
    working = [] # a temporary list for sorting
    for game in Game.games:
        working.append(game)
        if sort: # user indicated a sort method
            if sort == 'players-low':
                working = sorted(working, key=sort_by) # should sort by each object's players attr
            elif sort == 'players-high':
                working = sorted(working, reverse=True, key=sort_by)
    for game in working: #this is now a sorted list of object instances
        gamestring = '**{}**: {} players'.format(game.name, game.players) # will show the game name in bold
        message.append(gamestring)

    return to_final_string(message)


class Tabletop(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def gamelist(self, ctx, sort=None): # prints list of games; optional sort by playercount
        if sort: #if user requested a sort method
            message = generate_gamelist(sort)
        else:
            if Game.games_message:
                message = Game.games_message
            else:
                message = generate_gamelist()

        await ctx.channel.send(message)


    @commands.command()
    async def add_game(self, ctx, name, players=3, note=''):
        try:
            newObj = Game(name, players, note)
            await ctx.channel.send('Successfully added {}!'.format(name))
        except:
            await ctx.channel.send('Something went wrong!')
        save_games()


    @add_game.error
    async def add_game_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.channel.send('Error! If the game\'s name has spaces, try wrapping it in quotes.')


    @commands.command()
    async def delete_game(self, ctx, name):
        # delete the game
        save_games()


def setup(bot):
    bot.add_cog(Tabletop(bot))


read_games() #this should take place when the cog is loaded
