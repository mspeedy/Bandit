from lxml import html
import requests


# Currently broken
def scrape():
    dbFile = open(".\\scraper_output\\caa_partial-output.txt", "w+")

    genres = ["pop", "rock", "hip-hop", "electronic", "rb"]

    for genre in genres:
        print('https://touring.caa.com/artists/genres/' + genre)
        page = requests.get('https://touring.caa.com/artists/genres/' + genre, headers={'User-Agent': 'test'})
        tree = html.fromstring(page.content)

        # This will create a list of artists:
        artists = tree.xpath('//a[@class="no-underline gray-text artists"]/text()')
        print(artists)
        for artist in artists:
            if len(artist) > 1:
                dbFile.write(artist + "\n");

    dbFile.close()
