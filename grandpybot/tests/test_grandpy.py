from ..grandpy import Grandpy
import pytest
import json

class TestGrandpy:

    def setup_method(self):
        self.grandpy = Grandpy()
        self.user_input = "Salut GrandPy ! Par hasard, est-ce que tu connais l'adresse d'OpenClassrooms ?" 

    def test_grandpy_answer(self):
        # TODO Mock for APIs calls
        grandpy_answer = self.grandpy.grandpy_answer(self.user_input)
        try:
            data = json.loads(grandpy_answer)
            print(data)
        except ValueError:
            pytest.fail("Unexpected ValueError")
