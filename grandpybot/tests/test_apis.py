from grandpybot.utils.apis import search_address, search_mediawiki
import pytest

class TestApis:

    def setup_method(self):
        self.address_keywords = ["adresse", "openclassrooms", "france"]
        self.location = "Cité Paradis"

    def test_search_address(self):
        # TODO Mock for api calls
        assert search_address(self.address_keywords) is not None

    def test_search_mediawiki(self):
        # TODO Mock for api calls
        assert search_mediawiki(self.location) is not None

