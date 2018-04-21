from lxml import html
import requests


def scrape():
    dbFile = open(".\\scraper_output\\billions_full-output.txt", "w+")

    page = requests.get('http://billions.com/news/', headers={'User-Agent': 'test'})
    tree = html.fromstring(page.content)

    # This will create a list of artists:
    artists = tree.xpath('//div[@id="roster-all"]/ul/li/a/text()')

    for artist in artists:
        if len(artist) > 1:
            dbFile.write(artist + "\n");

    dbFile.close()
