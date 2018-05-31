from utils.parser import Parser
from utils.apis import search_address, search_mediawiki

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
        address = None
        extract = None
        question = self._search_question(user_raw_text)
        keywords = self.parser.get_keywords(question)
        # TODO look for an address if None, try with less words or country
        address = search_address(keywords)
        if address is not None:
            extract = self._get_extract(address)
            print(extract)
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
        road = filter(lambda x: x.isalpha(), adress.split(',')[0])
        road_name = ''.join([i for i in road if not i.isdigit()]).strip()
        extract = search_mediawiki(road_name)
        return extract

    def _format_grandpy_answer(self, address, extract):
        """
            Return all elements of Grandpy answer as a JSON Object
        """
        # ajouter lien page https://fr.wikipedia.org/wiki?curid=5653202
        answer = {}
        answer['address'] = address
        answer['extract'] = extract
        return json.dumps(answer)

    def _get_address(self, keywords, country="France"):
        # address = search_address(keywords)
        # address == None:
        pass
            


if __name__ == "__main__":
    my_gp = Grandpy()
    my_gp.grandpy_answer("Salut GrandPy ! Par hasard, est-ce que tu connais l'adresse d'OpenClassrooms ?")
