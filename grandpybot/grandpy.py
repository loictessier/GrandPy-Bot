from .utils.parser import Parser
from .utils.apis import search_address, search_mediawiki

from fuzzywuzzy import fuzz
import json


INTERROGATION_TERMS = ["que", "où", "comment", "à", "quel", "quelle", "demander", "demandais"]


class Grandpy:
    """
        GrandpyBot
    """

    def __init__(self):
        self.parser = Parser()

    def grandpy_answer(self, user_raw_text):
        """
            Grandpy try to answer the user by looking for the question terms
            then finding the address corresponding and informations about it
        """
        countries = ["France"]
        address = None
        extract = None
        # Seek a question out of the user input
        question = self._search_question(user_raw_text)
        # Extract keywords from the question
        keywords = self.parser.get_keywords(question)
        # Search for an address based on the keywords
        address = self._get_address(keywords, countries)
        # If an address was found, search for informations about the location
        if address is not None:
            extract = self._get_extract(address)
        # return all informations found as a json object
        return self._format_grandpy_answer(address, extract)

    def _search_question(self, raw_text):
        """
            Try to get the first question out of a raw text and return it
        """
        sentences = self.parser.raw_to_sentences(raw_text)
        for s in sentences:
            if self._is_question(s):
                return s
        return None

    def _is_question(self, sentence):
        """
            Return True if the sentence passed as parameter is considered
            as a question
        """
        for word in sentence.split():
            if any(fuzz.ratio(word, term) >= 90 for term in INTERROGATION_TERMS):
                return True
        return False

    def _get_extract(self, address):
        """
            Try to get informations (extract) about the road name of the
            address passed as parameter and return it
        """
        road = (address.split(',')[0]).split(' ')
        road_name = ' '.join([i for i in road if not i.isdigit()]).strip()
        media_wiki_result = search_mediawiki(road_name)
        if media_wiki_result != None:
            return search_mediawiki(road_name).split("\n")[-1].strip()
        return None

    def _format_grandpy_answer(self, address, extract):
        """
            Return all elements of Grandpy answer as a JSON Object
        """
        # ajouter lien page https://fr.wikipedia.org/wiki?curid=5653202
        answer = {}
        answer['address'] = address
        answer['extract'] = extract
        return json.dumps(answer)

    def _get_address(self, keywords, countries):
        address = self._search_try(keywords[:])
        if address != None:
            return address
        for country in countries:
            keywords.append(country)
            address = self._search_try(keywords[:])
            if address != None:
                return address
        return address

    def _search_try(self, keywords):
        while True:
            address = search_address(keywords)
            if address != None or len(keywords) < 1:
                return address
            else:
                keywords.pop(0)
