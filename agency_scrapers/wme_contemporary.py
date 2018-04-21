from lxml import html
import requests


def scrape():
    dbFile = open(".\\scraper_output\\wme_contemporary-output.txt", "w+")

    page = requests.get('http://wmeentertainment.com/expertise/music/contemporary/', headers={'User-Agent': 'test'})
    tree = html.fromstring(page.content)

    # This will create a list of artists:
    artists = tree.xpath('//div[@class="listing animate"]/a/ul/li/span/text()')

    for artist in artists:
        if len(artist) > 1:
            dbFile.write(artist + "\n");

    dbFile.close()
