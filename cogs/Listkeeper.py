# Cog to keep track of lists made by users

# import discord
# from discord.ext import commands
import asyncio
import os
import json

from typing import Union, Dict, List


## CLASS DEFS ##
class ColxItem():

    def __init__(self, label:str, note:str="") -> None:
        self.label: str = label
        self.note: str = note


    def __repr__(self) -> str:
        return f"(Item) {self.label}"


    def set_label(self, label:str) -> None:
        self.label = label


    def set_note(self, note:str) -> None:
        self.note = note


    def printout(self) -> str:
        return f"{self.label}: {self.note}"



class Collection():

    master: List[ColxItem] = []
    selected_list: Union[List[ColxItem], None] = None

    def __init__(self, name, desc) -> None:
        self.name: str = name
        self.desc: str = desc
        self.contents: List[ColxItem] = []

        Collection.master.append(self)
        Collection.selected_list = self


    def __repr__(self) -> str:
        return f"(Collection Object) {self.name}: {self.desc}"


    def delete_self(self) -> None:
        print(f'Removing {self.name} from Listkeeper!')
        Collection.master.remove(self)
        if Collection.selected_list == self:
            Collection.selected_list = None


    def add_item(self, label:str, note:str="") -> None: #
        for item in self.contents:
            if item.label == label:
                print("ERROR: Label already in use!")
                return

        item: ColxItem = ColxItem(label, note)
        self.contents.append(item)
        save_to_file()


    def delete_item(self, label:str) -> None:
        for item in self.contents:
            if item.label == label:
                print("removing", item.label)
                self.contents.remove(item)



## HELPER FUNCTIONS ##
def read_from_file() -> str: # I think this will return the file contents as str, maybe not
    pass


def save_to_file() -> None:
    pass


# ## MAIN COG ##
# class ListKeeper(commands.cog):

#     def __init__(self, bot) -> None:
#         self.bot = bot


#     def dir_init(self, ctx) -> None:
#         # check for directory exists
#         # if os.path.isdir(str(ctx.message.guild.id)):
#         #   ctx.channel.send('All set up!')
#         # else:
#         #   ctx.channel.send('Setting up folder!')
#         #   make folder
#         pass


#     @commands.command()
#     def list(self, ctx, colx_name=None) -> None:
#         # if not colx_name: return [self.name for name in List.master]
#         # else: 1)Find where List.master.name == colx_name and return that obj; 2)Return that obj info
#         pass