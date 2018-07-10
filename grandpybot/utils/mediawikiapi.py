import requests

from config import WIKI_SEARCH_URL
from .exceptions import ZeroResultsException, NoResponseException


class MediaWikiApi:

    @staticmethod
    def search(keywords):
        '''
            Call MediaWiki API with keywords and returns first result page id
        '''
        search_id_parameters = {
            "action": "query",
            "list": "search",
            "srsearch": keywords,
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

    @staticmethod
    def get_extract(page_id):
        '''
            Call MediaWikiApi and get an extract of the page corresponding
            to the id
        '''
        get_extract_parameters = {
            "action": "query",
            "pageids": page_id,
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
                extract = data["query"]["pages"][page_id]["extract"]
            except KeyError:
                raise ZeroResultsException
            return extract
        else:
            raise NoResponseException
