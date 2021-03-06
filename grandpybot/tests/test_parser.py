from grandpybot.utils.parser import Parser
import pytest


class TestParser:

    def setup_method(self):
        self.test_parser = Parser()
        self.raw_text = (
            "Salut GrandPy ! Par hasard, est-ce que tu connais"
            " l'adresse d'OpenClassrooms ?")
        self.sentence = "Est-ce que tu connais l'adresse d'OpenClassrooms ?"

    def test_raw_to_sentences(self):
        assert len(
            self.test_parser.raw_to_sentences(self.raw_text)) == 3
        assert self.test_parser.raw_to_sentences(
            self.raw_text)[0] == "Salut GrandPy !"
        assert self.test_parser.raw_to_sentences(
            self.raw_text)[1] == "Par hasard"
        assert self.test_parser.raw_to_sentences(
            self.raw_text)[2] == (
                "est-ce que tu connais l'adresse d'OpenClassrooms ?")

    def test_get_keywords(self):
        keywords = \
            [w.lower() for w in self.test_parser.get_keywords(self.sentence)]
        assert keywords == ["connais", "adresse", "openclassrooms"]
