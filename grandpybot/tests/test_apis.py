from grandpybot.utils.apis import search_address, search_mediawiki
import pytest

class TestApis:

    def setup_method(self):
        self.address_keywords = ["adresse", "openclassrooms", "france"]
        self.location = "Cité Paradis"

    def test_search_address(self):
        # mock avec monkeypatch le test de l'api
        assert search_address(self.address_keywords) is not None

    def test_search_mediawiki(self):
        # mock avec monkeypatch le test de l'api
        assert search_mediawiki(self.location) is not None

# mocker soir requests.get() soit ma propre fonction qui retourne la reponse de l'API