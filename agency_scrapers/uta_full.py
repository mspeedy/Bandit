from lxml import html
import requests


def scrape():
    dbFile = open(".\\scraper_output\\uta_full-output.txt", "w+")

    page = requests.get('http://music.utatouring.com/full-roster/', headers={'User-Agent': 'test'})
    tree = html.fromstring(page.content)

    # This will create a list of artists:
    artists = tree.xpath('//div[@class="ut-one-third"]/div/a/text()')
    for artist in artists:
        if len(artist) > 1:
            dbFile.write(artist + "\n");

    dbFile.close()
