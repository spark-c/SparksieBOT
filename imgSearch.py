# Draft code for Baby Bot discord bot. !cat command that searches 'cat'
# in google and returns a random image link.
# 8/11/2020
# Python 3.8
# Collin Sparks

import requests
import bs4
'''
query = 'cat' # add function to randomly select cat query from list
results = requests.get(r'https://google.com/search?tbm=isch&q={0}'.format(query))
#try:
results.raise_for_status()

#except:
#    print('ERROR downloading search results')


parsed = bs4.BeautifulSoup(results.text, 'html.parser')
images = parsed.select('img')
imgLink = images[1].attrs['src']
print(imgLink)
'''

query = 'cat' # add function to randomly select cat query from list
results = requests.get(r'https://google.com/search?tbm=isch&q={0}'.format(query))
#try:
results.raise_for_status()
#except:

parsed = bs4.BeautifulSoup(results.text, 'html.parser')
print(parsed)
samples = parsed.find_all('a', class_='mM5pbd')
target = samples[0]
link = target.attr['href']

finalPage = requests.get(r'https://google.com{0}'.format(link))
finalPage.raise_for_status()

realImg = bs4.BeautifulSoup(finalPage.text, 'html.parser')
element = realImg.select('.irc_mi')
final = element.attr['src']
print('final URL is: '.format(final))


