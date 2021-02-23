# baby-bot
baby's first discord bot

This is a discord bot made initially as a learning project; it is a part of the discord server I've set up with friends of mine, and I add various functionalities as needed.

Commands:

....(Funtions cog)

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

....(Minecraft cog)

!playercount - returns the number of players currently connected to the Baby Blue Minecraft server. Optionally takes the argument "names" to return the players' usernames as well (!playercount names).

....(Tabletop cog)

!gamelist: returns the list of boardgames we've assembled.
You can optionally type players-low or players-high (!gamelist players-low) to sort the list by the required number of players.

  When you specify number of players, use a low number that is reasonable for having fun playing the game. So like, you can technically play Monopoly with 2 players, but why would you do that? I'd say 3 for that one.

  If no #players is specified, it will default to 3.

!add_game: adds a game to the list. Usage: !add_game (name) (# players) (optional note).
Keep in mind that any item that has a space in it will NEED to be wrapped in quotes. E.g. Secret Hitler will not work; must be "Secret Hitler". Also applies to the optional note.

!delete_game: type the game's name after this command to remove it from the list.

Currently there is no way to view the notes, or edit the game's info; that stuff is still being worked on.

TBD: Finish ist of commands and functionality.
