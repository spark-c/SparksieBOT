import utils.logger
import os
import bot as sb

bot = sb.bot
sb.initialize_bot(bot)

try:
    # When running locally
    with open(r'./baby-bot-token.txt', 'r') as f:
        token: str = f.read()
    bot.run(token)
except:
    # When deployed, with envvars
    bot.run(os.environ["TOKEN"])