
def searchByArtistName(sp, artistName):
    results = sp.search(q='artist:'+artistName, type='artist')
    return results


def searchByArtistId(sp, artistId):
    results = sp.artist(artistId)
    return results


def getArtistByName(sp, artistName):
    """

    :param sp:
    :param artistName:
    :return: Spotify Artist Object
    """
    spotifyInfo = searchByArtistName(sp, artistName)
    indexCount = 0
    for artistInfo in spotifyInfo["artists"]["items"]:
        if artistInfo["name"].lower() == artistName.lower():
            return spotifyInfo["artists"]["items"][indexCount]
        else:
            indexCount += 1

    return None


def getSpotifyFollowers(artist):
    """

    :param sp: spotify access token
    :param artist: Artist name
    :return: number of followers for the given artist
    """
    if artist:
        return str(artist["followers"]["total"])
    return "0"


def getSpotifyGenre(artist):
    if artist and artist["genres"]:
        return artist["genres"][0]
