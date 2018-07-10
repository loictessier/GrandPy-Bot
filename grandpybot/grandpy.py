from .utils.parser import Parser
from .utils.googleapi import GoogleApi
from .utils.mediawikiapi import MediaWikiApi
from .utils.exceptions import ZeroResultsException, NoResponseException

from fuzzywuzzy import fuzz
import json


INTERROGATION_TERMS = [
    "que", "où", "comment", "à", "quel", "quelle", "demander", "demandais"]

GRANDPY_PRESET_ANSWER = {
    "tired_grandpy":
        "Je suis fatigué, je répondrai à tes questions une autre fois !",
    "ignorant_grandpy":
        "Je ne me souviens pas d'un tel endroit.",
    "tired_for_story_grandpy":
        "Je suis trop fatigué pour te raconter une histoire sur cet endroit.",
    "ignorant_for_story_grandpa":
        "Je n'ai pas d'histoire à raconter sur cet endroit.",
    "no_question_detected":
        "Désolé, je n'ai pas compris la question."
}


class Grandpy:
    """
        The logic for the grandpy bot parsing and response construction
    """

    def __init__(self):
        self.parser = Parser()

    def grandpy_answer(self, user_raw_text):
        """
            Grandpy try to answer the user by looking for the question terms
            then finding the address corresponding and informations about it
        """
        if user_raw_text == "":
            return self._format_grandpy_answer("", "", "", "")
        countries = ["France"]
        address = None
        extract = None
        lien = None
        # Seek a question out of the user input
        question = self._search_question(user_raw_text)
        # Extract keywords from the question
        keywords = self.parser.get_keywords(question)
        # Search for an address based on the keywords
        if keywords is not None:
            address = self._get_address(keywords, countries)
        else:
            address = GRANDPY_PRESET_ANSWER["no_question_detected"]
        # If an address was found, search for informations about the location
        if address is not None and (
                address not in GRANDPY_PRESET_ANSWER.values()):
            page_id = self._search_wiki_page(address["formatted_address"])
            extract = self._get_extract(page_id)
            if page_id != "" and page_id is not None:
                lien = "https://fr.wikipedia.org/wiki?curid=" + page_id
            # return all informations found as a json object
            return self._format_grandpy_answer(
                address["formatted_address"],
                extract,
                lien,
                address["geometry"]["location"])
        if address is None:
            address = GRANDPY_PRESET_ANSWER["ignorant_grandpy"]
        return self._format_grandpy_answer(address, "", "", "")

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
            if any(fuzz.ratio(word.lower(), term.lower()) >= 90
                    for term in INTERROGATION_TERMS):
                return True
        return False

    def _search_wiki_page(self, address):
        """
            Call MediaWikiApi class search method to get informations
            about the road name.
        """
        road = (address.split(',')[0]).split(' ')
        road_name = ' '.join([i for i in road if not i.isdigit()]).strip()
        try:
            wiki_page_id = MediaWikiApi.search(road_name)
        except ZeroResultsException:
            wiki_page_id = ""
        except NoResponseException:
            wiki_page_id = ""
        return wiki_page_id

    def _get_extract(self, wiki_page_id):
        """
            Try to get informations (extract) about the road name of the
            address passed as parameter and return it
        """
        try:
            media_wiki_result = (
                MediaWikiApi.get_extract(wiki_page_id).split("\n")[-1].strip()
            )
        except ZeroResultsException:
            media_wiki_result = GRANDPY_PRESET_ANSWER[
                "ignorant_for_story_grandpa"
            ]
        except NoResponseException:
            media_wiki_result = GRANDPY_PRESET_ANSWER[
                "tired_for_story_grandpy"
            ]
        return media_wiki_result

    def _format_grandpy_answer(self, address, extract, lien, geo_location):
        """
            Return all elements of Grandpy answer as a JSON Object
        """
        answer = {}
        answer['address'] = address
        answer['extract'] = extract
        answer['lien'] = lien
        answer['location'] = geo_location
        return answer

    def _get_address(self, keywords, countries):
        """
            Call search_try to get an address and
            loop over keywords combination until he finds one
        """
        address = self._search_try(keywords[:])
        if address is not None:
            return address
        for country in countries:
            keywords.append(country)
            address = self._search_try(keywords[:])
            if address is not None:
                continue
        if address is None:
            address = GRANDPY_PRESET_ANSWER["ignorant_grandpy"]
        return address

    def _search_try(self, keywords):
        """
            Try to get an adresse from a keywords combination
        """
        while True:
            try:
                address = GoogleApi.search(keywords)
            except ZeroResultsException:
                address = None
            except NoResponseException:
                return GRANDPY_PRESET_ANSWER["tired_grandpy"]

            if address is not None or len(keywords) < 1:
                return address
            else:
                keywords.pop(0)
