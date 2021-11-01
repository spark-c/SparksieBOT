# commands for Functions cog, independent of Discord api
import discord
import random
from typing import List


def roll(dice: str) -> List[int]:
    try:
        iters: int
        die_size: int
        iters, die_size = [int(num) for num in dice.split('d')] # 4d6 = [4, 6] 
    except:
        # TODO raise better errors
        raise Exception
    
    values: List[int] = list()
    for i in range(0, iters):
        values.append(random.randint(1, die_size))

    return values


def marco(ctx) -> discord.TextChannel:
    textChannels: List[discord.TextChannel] = list(
        filter( # filter() returns an iterator
            lambda channel: channel.type == discord.ChannelType.text,
            ctx.guild.channels
        )
    )
    if len(textChannels) == 1:
        return textChannels[0]
    else:
        textChannels.remove(ctx.channel)
        return random.choice(textChannels)