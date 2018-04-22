import sys
import os.path
import datetime
import spotipy
import spotipy.util as util
import spotify.lib.search as spsearch
import agency_scrapers.scraper as scrape
from songkick.search import *
from config import SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI


def main():
    scope = 'user-library-read';

    iniVals = getIniVals()

    username = iniVals["SPOTIFY_USERNAME"]
    print("Getting token")
    token = util.prompt_for_user_token(username, scope,
                                       client_id=SPOTIPY_CLIENT_ID,
                                       client_secret=SPOTIPY_CLIENT_SECRET,
                                       redirect_uri=SPOTIPY_REDIRECT_URI)
    print("Got token: " + str(token))

    if token:
        sp = spotipy.Spotify(auth=token);
        # results = search.searchByArtistName(sp, 'Laura Stevenson');
        while True:
            response = input("Please enter a command (report):");
            if response == 'report':
                makeReport(sp)
            elif response == 'search':
                search(sp)
            elif response == 'q' or response == 'quit':
                break;
            else:
                displayHelp()
        # Pass sp into other functions for desired functionality
    else:
        print("Can't get token for", username)


def makeReport(sp):
    agency = input("Enter the agency: ")
    roster = input("Enter the roster(full): ")
    doScrape(agency, roster);
    dbFile = open('./scraper_output/' + agency + '_' + roster + '-output.txt', 'r')
    print('Creating report for ' + agency + '_' + roster + '...')
    reportFile = open(makeReportFileName(agency, roster), 'w+')
    reportFile.write('"ArtistName",TotalSpotifyFollowers\n')
    delim = ','
    for artist in dbFile:
        artist = artist.strip()
        if followers:
            reportFile.write('"' + artist + '"' + delim + followers + '\n')
        else:
            reportFile.write('"No information found for: ' + artist + '",-1\n')
        followers = None
    reportFile.close()
    dbFile.close()


def getSpotifyFollowers(sp, artist):
    """

    :param sp: spotify access token
    :param artist: Artist name
    :return: number of followers for the given artist
    """
    spotifyInfo = spsearch.searchByArtistName(sp, artist)
    indexCount = 0
    for artistInfo in spotifyInfo["artists"]["items"]:
        if artistInfo["name"].lower() == artist.lower():
            return str(spotifyInfo["artists"]["items"][indexCount]["followers"]["total"])
        else:
            indexCount += 1

    return None


def doScrape(agency, roster):
    print('Scraping for ' + agency + '_' + roster + '...')
    scrape.scrapeAgency(agency, roster)


def makeReportFileName(agency, roster):
    now = datetime.datetime.now()
    return './reports/' + \
           'report_' + \
           now.strftime("%Y-%m-%d") + '_' + \
           now.strftime("%H-%M-%S") + '_' + \
           agency + '-' + \
           roster + \
           '.csv'


def displayHelp():
    print('Welcome to Bandit! You can currently use the "report", "help", search, and "quit" functions')


# Creates a map of all values in the main ini file
def getIniVals():
    file = open('./ini/main.ini', 'r')
    valueMap = {}
    for line in file:
        if len(line) > 2:
            lineParts = line.split("=")
            valueMap[lineParts[0]] = lineParts[1]
    return valueMap


def search(sp):
    metro = input('Enter the metro area you\'d like to search in: ')
    metroId = findMetroAreaId(metro)
    startDate = strToDate(input('Enter the earliest date you\'d like to search for (YYYY-MM-DD): '))
    endDate = strToDate(input('Enter the latest date you\'d like to search for. ' +
                    'This can be the same as the earliest. (YYYY-MM-DD):'))
    print('Searching for bands available these days...')
    artists = freeArtistsByDate(metroId, startDate, endDate)

    artists = sorted(artists, key=lambda x: x['availableDate'])
    for artist in artists:
        followers = getSpotifyFollowers(sp, artist["displayName"])
        print(dateToStr(artist["availableDate"]) + "\t| " + artist["displayName"] + "\t\t| " + str(followers) + " followers")


main()
