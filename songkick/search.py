import json
import requests
from songkick.config import SONGKICK_API_KEY


url = "http://api.songkick.com/api/3.0/"

def results(obj):
    """
    Converts JSON object to a python library and depaginates
    :param obj: A raw response from the songkick API
    :return: the 'results' dictionary within a response, a list of dictionaries
    """
    return json.loads(obj.content)["resultsPage"]["results"]


def findMetroAreaId(loc):
    """
    :param loc: string for a location, e.g. 'Boston'
    :return: The Metro Area ID for location loc.
    """
    location = requests.get(url + "search/locations.json?query=" + loc + "&apikey=" + SONGKICK_API_KEY)
    return results(location)["location"][0]["metroArea"]["id"]


def findMetroShows(metroId):
    """
    :param metroId: Metro Area ID to search
    :return: list of dictionaries with each dictionary being an 'Event' type object
    """
    return getDepaginatedEvents(url + "metro_areas/" + str(metroId) + "/calendar.json?apikey=" + SONGKICK_API_KEY)


def getDepaginatedEvents(requesturl, pagenum=1):
    """
    :param requesturl: The songkick API url to fetch data from
    :param resulttype: The type of the songkick objects expected (e.g. 'event')
    :param pagenum: the page number, base case of 1, recursively increases to get all pages
    :return: A list of songkick objects as python dictionaries
    """
    resp = requests.get(requesturl, {"per_page": 50, "page": pagenum})
    respPy = json.loads(resp.content)
    if respPy["resultsPage"]["totalEntries"] > pagenum * 50:
        return respPy["resultsPage"]["results"]["event"] + getDepaginatedEvents(requesturl, pagenum + 1)
    else:
        return respPy["resultsPage"]["results"]["event"]


def findShowArtists(shows):
    """
    :param shows: list of Event objects
    :return: list of Artist IDs for all artists performing at @shows
    """
    artists = []
    for show in shows:
        for performance in show["performance"]:
            artists.append((performance["displayName"], performance["artist"]["id"]))

    return artists



bostonId = findMetroAreaId("boston")

bostonShows = findMetroShows(bostonId)

bostonArtists = findShowArtists(bostonShows)

print(bostonArtists)


