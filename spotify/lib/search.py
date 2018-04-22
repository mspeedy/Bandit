
def searchByArtistName(sp, artistName):
    results = sp.search(q='artist:'+artistName, type='artist')
    return results;


def searchByArtistId(sp, artistId):
    results = sp.artist(artistId)
    return results;


def getSpotifyFollowers(sp, artistName):
    """

    :param sp: spotify access token
    :param artist: Artist name
    :return: number of followers for the given artist
    """
    spotifyInfo = searchByArtistName(sp, artistName)
    indexCount = 0
    for artistInfo in spotifyInfo["artists"]["items"]:
        if artistInfo["name"].lower() == artistName.lower():
            return str(spotifyInfo["artists"]["items"][indexCount]["followers"]["total"])
        else:
            indexCount += 1

    return None
