# parses args for baby-bot functions
import argparse


# Overriding ArgumentParser's default behavior of
# printing err msg to stdout and sys.exit()ing.
# That's not helpful to us, since we can't see stdout from discord.
class ArgumentError(Exception):
    def __init__(self, message: str, usage: str) -> None:
        self.message: str = message
        self.usage: str = usage
        super().__init__(self.message)


class LoudArgumentParser(argparse.ArgumentParser):
    def error(self, message) -> None:
        usage: str = (
            self.format_usage()
            .replace("usage: cmdparser.py [-h] ", "")
            .replace("\n", "")
        )
        raise ArgumentError(message, usage)


## Listkeeper parsers
newlist: LoudArgumentParser = LoudArgumentParser(description="Creates a new list.")
newlist.add_argument(
    "list_name",
    metavar="<list-name>",
    help="Name of the list you'd like to create"
)
newlist.add_argument(
    "list_description",
    metavar="<list-description>",
    help="An optional note to attach to the list",
    nargs="?",
    default=None
)

additem: LoudArgumentParser = LoudArgumentParser(description="Adds an item to a list.")
additem.add_argument(
    "-l", "-list", 
    metavar="<list-name>", 
    help="Name of the list you'd like to modify"
)
additem.add_argument(
    "item_name", 
    metavar="<item-name>", 
    help="Name of the new item to create"
)
additem.add_argument(
    "item_description", 
    metavar="<item-description>", 
    help="An optional note to attach to the item", 
    nargs="?", 
    default=None
)

list: LoudArgumentParser = LoudArgumentParser(description="Displays the given (or most recently used) list.")
list.add_argument(
    "list_name",
    nargs="?",
    metavar="<list-name>", 
    help="Name of the list you'd like to display"
)

rmlist: LoudArgumentParser = LoudArgumentParser(description="Deletes the given list.")
rmlist.add_argument(
    "list_name",
    metavar="<list-name>",
    help="Name of the list you'd like to delete"
)

rmitem: LoudArgumentParser = LoudArgumentParser(description="Deletes an item from a list.")
rmitem.add_argument(
    "-l", "-list", 
    metavar="<list-name>", 
    help="Name of the list you'd like to modify"
)
rmitem.add_argument(
    "item_name",
    metavar="<item-name>", 
    help="Name of the item to delete"
)

def fail() -> None:
    try:
        additem.parse_args(["little", "cindy", "lou", "who"])
    except ArgumentError as e:
        print("ERROR! Here:\n", e, "\n", e.usage)