from lxml import html
import requests


def scrape():
    paradigm_lists = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s",
                      "t", "u", "v", "w", "x", "y", "z", "0"]
    dbFile = open(".\\scraper_output\\paradigm_full-output.txt", 'w+')

    for list in paradigm_lists:
        page = requests.get("http://www.paradigmagency.com/music/list/" + list + "/", headers={'User-Agent': 'test'})
        tree = html.fromstring(page.content)
        # This will create a list of artists:
        artists = tree.xpath('//div[@class="grid grid--condensed"]/div/div/h3/text()')
        for artist in artists:
            if len(artist) > 1:
                try:
                    dbFile.write(artist.strip() + "\n")
                except UnicodeEncodeError:
                    print('Encoding error on: ' + artist.strip())
    print('\n')
    dbFile.close();
