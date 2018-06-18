import requests

from ..constants import GOOGLE_SEARCH_URL, GOOGLE_API_KEY, WIKI_SEARCH_URL


def search_address(*address_keywords):
    '''Call google maps api with keywords and returns an address'''
    # TODO return lat/long
    parameters = {
        "query": "+".join(*address_keywords),
        "key": GOOGLE_API_KEY
    }
    response = requests.get(GOOGLE_SEARCH_URL, params=parameters)
    if response.ok:
        response.encoding = 'UTF-8'
        data = response.json()
        if data["status"] == 'ZERO_RESULTS' or len(data["results"]) < 1:
            raise ZeroResultsException
        else:
            return data["results"][0]["formatted_address"]
    else:
        raise NoResponseException


def search_mediawiki_page(location):
    '''Call MediaWiki API with keyword and returns an page id'''
    # TODO return id of wiki page to display a link
    search_id_parameters = {
        "action": "query",
        "list": "search",
        "srsearch": location,
        "srlimit": "1",
        "format": "json"
    }
    response = requests.get(WIKI_SEARCH_URL, params=search_id_parameters)
    if response.ok:
        response.encoding = "UTF-8"
        data = response.json()
        try:
            return str(data["query"]["search"][0]["pageid"])
        except KeyError:
            raise ZeroResultsException
    else:
        raise NoResponseException


def get_media_wiki_extract(pageid):
    '''get an extract of the page corresponding to the id'''
    get_extract_parameters = {
        "action": "query",
        "pageids": pageid,
        "prop": "extracts",
        "explaintext": "true",
        "exsectionformat": "plain",
        "exsentences": "3",
        "format": "json"
    }
    response = requests.get(WIKI_SEARCH_URL, params=get_extract_parameters)
    if response.ok:
        response.encoding = "UTF-8"
        data = response.json()
        try:
            extract = data["query"]["pages"][pageid]["extract"]
        except KeyError:
            raise ZeroResultsException
        return extract
    else:
        raise NoResponseException


class ZeroResultsException(Exception):
    """Raised when the request returns zero values"""
    pass


class NoResponseException(Exception):
    """Raised when there is no response for the api"""
    pass
