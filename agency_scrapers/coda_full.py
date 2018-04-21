from lxml import html
import requests


def scrape():
    dbFile = open(".\\scraper_output\\coda_full-output.txt", "w+")

    page = requests.get('http://www.codaagency.com/roster/artist', headers={'User-Agent': 'test'})
    tree = html.fromstring(page.content)

    # This will add all artists on the roster to the dbFile
    artists = tree.xpath('//div[@class="letter_list"]/ul/li/a/text()')
    for artist in artists:
        if len(artist) > 1:
            try:
                dbFile.write(artist + "\n")
            except UnicodeEncodeError:
                print('Encoding error on: ' + artist)

    dbFile.close()
