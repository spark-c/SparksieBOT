import utils.logger
import sys
import os
import bot as sb


bot = sb.bot

# -c flag to specify which cogs to load on startup.
# else statement holds defaults.
if len(sys.argv) > 2 and sys.argv[1] in ["-c", "--cogs"]:
    sb.initialize_bot(bot, load_cogs=sys.argv[2:])
else:
    sb.initialize_bot(bot, load_cogs=["Functions", "Listkeeper", "ApiCalls"])

try:
    # When running locally
    with open(r'./baby-bot-token.txt', 'r') as f:
        token: str = f.read()
    bot.run(token)
except:
    # When deployed, with envvars
    bot.run(os.environ["TOKEN"])