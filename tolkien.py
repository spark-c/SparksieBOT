## draft code for grabbing random Tolkien quotes

import random
import requests
import bs4

    @commands.command()
    async def lotr(self): #grabs a random quote from source site
        queryIndex = random.randint(1, 64) #there are 64 quotes on the site
        results = requests.get(r'http://lotrproject.com/quotes/quote/{}'.format(queryIndex))

        try:
            results.raise_for_status()
        except:
            await ctx.channel.send("I couldn't find a quote!")
            return

        parsed = bs4.BeautifulSoup(results.text, 'html.parser')
        quote = parsed.select('.text').text
        character = parsed.select('.character').text
        source = parsed.select('.source').text

        quoteEmbed = discord.Embed(description = quote)
        quoteEmbed.add_field(name = character, value = source)

        ctx.channel.send(quoteEmbed)
