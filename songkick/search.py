import json
import requests
from config import SONGKICK_API_KEY
from songkick.utils import *

# http://api.songkick.com/api/3.0/search/locations.json?query=Boston&apikey=S8ZSPviCBeUKbmN0
url = "http://api.songkick.com/api/3.0/"


def findMetroAreaId(loc):
    """
    :param loc: string for a location, e.g. 'Boston'
    :return: The Metro Area ID for location loc.
    """
    location = requests.get(url + "search/locations.json?query=" + loc + "&apikey=" + SONGKICK_API_KEY)
    return json.loads(location.content)["resultsPage"]["results"]


def findMetroShows(metroId):
    """
    :param metroId: Metro Area ID to search
    :return: list of dictionaries with each dictionary being an 'Event' type object
    """
    return getDepaginatedEvents(url + "metro_areas/" + str(metroId) + "/calendar.json?apikey=" + SONGKICK_API_KEY)


def getDepaginatedEvents(requesturl, pagenum=1,
                         min_date=datetime.today() + timedelta(days=30),
                         max_date=datetime.today() + timedelta(days=120)):
    """
    :param requesturl: The songkick API url to fetch data from
    :param pagenum: the page number, base case of 1, recursively increases to get all pages
    :param min_date: datetime object of earliest date to search
    :param max_date: datetime object of latest date to search
    :return: A list of songkick events as python dictionaries
    """
    resp = requests.get(requesturl,
                        {"per_page": 50,
                         "page": pagenum,
                         "min_date": dateToStr(min_date),
                         "max_date": dateToStr(max_date)})
    respPy = json.loads(resp.content)
    if respPy["resultsPage"]["totalEntries"] > pagenum * 50:
        return respPy["resultsPage"]["results"]["event"] + getDepaginatedEvents(requesturl,
                                                                                pagenum=pagenum + 1,
                                                                                min_date=min_date,
                                                                                max_date=max_date)
    else:
        return respPy["resultsPage"]["results"]["event"]


def filterShowsByPopularity(shows, low=.003, high=.075):
    """
    Filter out shows that are not within given bounds of popularity. Useful for finding bands within your price range.
    :param shows: A list of Songkick Event objects
    :param low: lower bound of popularity, between 0 and 1
    :param high: upper bound of popularity, between 0 and 1
    :return: A list of Songkick events within the given bounds of popularity
    """
    filtered = []
    for show in shows:
        if high > show["popularity"] > low and show["type"] == "Concert":
            filtered.append(show)
    return filtered


def findShowArtists(shows):
    """
    :param shows: list of Event objects
    :return: List of Dictionaries of {artist name, artist id, show date}
    """
    artists = []
    for show in shows:
        for performance in show["performance"]:
            artists.append({"displayName":performance["displayName"],
                            "id":performance["artist"]["id"],
                            "showDate":show["start"]["date"]})

    return artists


def isFreeOn(artistId, date):
    """

    :param artistid: id of the artist to check
    :param date: datetime of the date to check
    :return:
    """
    strDate = dateToStr(date)
    resp = requests.get(url + "artists/" + str(artistId) + "/calendar.json?apikey=" + SONGKICK_API_KEY,
                        {"per_page": 1, "min_date": strDate, "max_date": strDate}
                        )
    if resp.status_code != 200:
        # If API call fails, try one more time (prevents some errors)
        resp = requests.get(url + "artists/" + str(artistId) + "/calendar.json?apikey=" + SONGKICK_API_KEY,
                            {"per_page": 1, "min_date": strDate, "max_date": strDate}
                            )
    return json.loads(resp.content)["resultsPage"]["totalEntries"] < 1


def bookableArtistDates(artists):
    """

    :param artists: List of dictionaries of {artist name, artist id, show date}
    :return: List of dictionaries of {artist name, artist id, unbooked date}
    """
    bookables = []
    for artist in artists:
        if isFreeOn(artist["id"], dayBefore(artist["showDate"])):
            bookables.append({"displayName": artist["displayName"],
                              "id": artist["id"],
                              "availableDate": dayBefore(artist["showDate"])})
        if isFreeOn(artist["id"], dayAfter(artist["showDate"])):
            bookables.append({"displayName":artist["displayName"],
                              "id":artist["id"],
                              "availableDate":dayAfter(artist["showDate"])})
    return bookables


def freeArtistsByDate(metroId, startDate, endDate):
    """
    Find artists in the city and available on a specific date
    :param metroId: the metro id of the city to search
    :param date: datetime object of the date to search
    :return: list of artists free on the given date {artist name, artist id, unbooked date}
    """

    resp = getDepaginatedEvents(url + "metro_areas/" + str(metroId) + "/calendar.json?apikey=" + SONGKICK_API_KEY,
                                min_date=startDate, max_date=endDate)
    resp = filterShowsByPopularity(resp)
    artists = findShowArtists(resp)
    bookables = bookableArtistDates(artists)

    return bookables



