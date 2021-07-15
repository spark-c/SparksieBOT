# parses args for baby-bot functions
import argparse


## Listkeeper parsers
additem = argparse.ArgumentParser(description="Adds an item to a list.")
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

list = argparse.ArgumentParser(description="Displays the given (or most recently used) list.")
list.add_argument("list_name",
    nargs="?",
    metavar="<list-name>", 
    help="Name of the list you'd like to display"
)

rmlist = argparse.ArgumentParser(description="Deletes the given list.")
rmlist.add_argument(
    "list_name",
    metavar="<list-name>",
    help="Name of the list you'd like to delete"
)

rmitem = argparse.ArgumentParser(description="Deletes an item from a list.")
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

