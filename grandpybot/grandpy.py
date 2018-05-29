from grandpybot.utils.parser import Parser
from grandpybot.utils.apis import search_address, search_mediawiki


class Grandpy:

    def __init__(self):
        self.parser = Parser()

    def grandpy_answer(self, user_raw_text):
        # get question out of the raw_text
        question = self._search_question(user_raw_text)
        # parse question to extract keywords
        keywords = self.parser.get_keywords(question)
        # search for an adress based on keyword
        address = search_address(keywords)
        # if an address is found search for informations about the location
        if address is not None:
            extract = self._get_extract(address)
        return self._format_grandpy_answer(address, extract)

    def _search_question(self, raw_text):
        # use parser to get sentences from raw_text
        # extract the question from the sentence
        pass

    def _get_extract(self, address):
        # extract road name from address
        # call search_mediawiki on the road name to get text
        # returns formatted text as a message from grandpy
        pass

    def _format_grandpy_answer(self, address, extract):
        # returns grandpy answer as json object 
        # ajouter lien page https://fr.wikipedia.org/wiki?curid=5653202
        pass