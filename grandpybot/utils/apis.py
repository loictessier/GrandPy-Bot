import requests

from ..constants import GOOGLE_SEARCH_URL, GOOGLE_API_KEY, WIKI_SEARCH_URL


def search_address(*address_keywords):
    """
        Call google maps api with keywords and returns an address
    """
    parameters = {
        "query": "+".join(*address_keywords),
        "key": GOOGLE_API_KEY
    }
    response = requests.get(GOOGLE_SEARCH_URL, params=parameters)
    if response.ok:
        response.encoding = 'UTF-8'
        data = response.json()
        if len(data["results"]) >= 1 :
            return data["results"][0]["formatted_address"]
    return None


def search_mediawiki(location):
    """
        Call MediaWiki API with keyword and returns an extract
    """
    # get the id of the first result on the search based on location
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
        if len(data["query"]["search"]) >= 1 :
            wiki_page_id = str(data["query"]["search"][0]["pageid"])
        else:
            return
    else:
        return None

    # get an extract of the page corresponding to the id
    get_extract_parameters = {
        "action": "query",
        "pageids": wiki_page_id,
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
        return data["query"]["pages"][wiki_page_id]["extract"]
    else:
        return None

