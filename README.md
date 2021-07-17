# baby-bot

A Discord bot that provides upkeep, utility, and some fun commands for my personal discord server!

Commands:

### (Funtions cog)
---
!cat: Returns a random cat picture. You can type something after '!cat' to search for that query instead of cat. Optional argument "-f" to return the first (read: most relevant) search result for your query.\
Usage: `!cat [-f] [<alternate-query>]`\
`!cat -f dog`

!marco: Pings you with 'Polo!' from a different text channel.\
Usage: `!marco`\
`!marco`\

!ping - Pong!\
Usage: `!ping`\
`!ping`\

!roll: "Rolls" some number of dice, of some given size.\
Usage: `!roll <num-dice>d<die-size>`\
`!roll 4d6`\

!say: Makes the bot say whatever you type after !say\
Usage: `!say <statement>`\
`!say hello, world`\

!sleepy: Turns bot off (confirm with a reply of 'y').\
Usage `!sleepy`\
`!sleepy`\

!teampicker: Returns numbers in the format [ 1, 2 ] vs [ 3, 4, 5 ] in random order to assign teams. Plans to optionally use names from an occupied voice channel instead.\
Usage: `!teampicker <team1size> <team2size>`\
`!teampicker 2 3`\

!help: Displays help message for all commands, or the specified command.\
Usage: `!help [<command-name>]`\
`!help` or `!help teampicker`\

TODO: Update code and documentation for `!help_printout` (shows this message)

### (Listkeeper cog)
---
!newlist: Creates a new list.\
Usage: `!newlist <list-name> [<list-description>]`\
`!newlist "My First List" "This is the first list that I have made."`


!additem: Adds an item to the selected list.\
Usage: `!additem [-l <list-name>] <item-name> [<item-note>]`\
`!additem -l "My First List" Item1 "The first item of the list"`\


!list: Prints out the entire selected list and its items.\
Usage: `!list [<list-name>]`\
`!list "My First List"`\


!listall: Shows all lists created on this server.\
`Usage: !listall`\
`!listall`\


!rmlist: Removes / Deletes a list.\
Usage: `!rmlist <list-name>` (list-name REQUIRED!)\
`!rmlist "My First List"`\


!rmitem: Removes / Deletes an item from a list.\
Usage: `!rmitem [-l <list-name>] <item-name>`\
`!rmitem -l "My First List" Item1`\

### (Minecraft cog)
---
!playercount: Returns the number of players currently connected to the Baby Blue Minecraft server. Optionally takes the argument "names" to return the players' usernames as well.\
Usage: `!playercount ["names"]`\
`!playercount names`

TBD: Finish ist of commands and functionality.
