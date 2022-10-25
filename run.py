import asyncio
import utils.logger
import sys
import os
import bot as sb


bot = sb.bot

async def main() -> None:
# -c flag to specify which cogs to load on startup.
# else statement holds defaults.
    if len(sys.argv) > 2 and sys.argv[1] in ["-c", "--cogs"]:
        await sb.initialize_bot(bot, load_cogs=sys.argv[2:])
    else:
        await sb.initialize_bot(bot, load_cogs=["Functions", "ApiCalls"])

    async with bot:
        try:
        # When running locally
            with open(r'./baby-bot-token.txt', 'r') as f:
                token: str = f.read()
            await bot.start(token)

        except:
            # When deployed, with envvars
            await bot.start(os.environ["TOKEN"])

asyncio.run(main())
