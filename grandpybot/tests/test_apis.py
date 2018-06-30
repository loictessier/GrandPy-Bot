from grandpybot.utils.apis import search_address, search_mediawiki_page, get_media_wiki_extract, ZeroResultsException, NoResponseException
import pytest

import requests


class MockResponse:
    '''Mock for requests.get response call'''
    def __init__(self, result, ok=True):
        self.ok = ok
        self.result = result

    def json(self):
        return self.result


class TestApis:
    '''Testing the apis functions calls'''

    def setup_method(self):
        self.address_keywords = ["adresse", "openclassrooms", "france"]
        self.location = "Cité Paradis"
        
    def test_search_address_ok(self, monkeypatch):
        def mockreturn(url, params):
            return MockResponse({ 
                    "results": 
                    [{ 
                        "formatted_address": "7 Cité Paradis, 75010 Paris, France"
                    }],
                    "status": "OK"
                })
        monkeypatch.setattr(requests, "get", mockreturn)
        assert search_address(self.address_keywords) is not None

    def test_search_address_zero(self, monkeypatch):
        def mockreturn(url, params):
            return MockResponse({
                    "status": "ZERO_RESULTS"
                })
        monkeypatch.setattr(requests, "get", mockreturn)
        with pytest.raises(ZeroResultsException):
            search_address(["adresse", "openclassrooms", "test"])

    def test_search_address_no_response(self, monkeypatch):
        def mockreturn(url, params):
            return MockResponse({}, False)
        monkeypatch.setattr(requests, "get", mockreturn)
        with pytest.raises(NoResponseException):
            search_address(self.address_keywords)

    def test_search_mediawiki_ok(self, monkeypatch):
        def mockreturn(url, params):
            return MockResponse({
                "query": {
                    "search": [
                        { "pageid": 5653202 }
                    ]
                }
            })
        monkeypatch.setattr(requests, "get", mockreturn)
        assert search_mediawiki_page(self.location) is not None

    def test_search_mediawiki_zero(self, monkeypatch):
        def mockreturn(url, params):
            return MockResponse({ "query": {} })
        monkeypatch.setattr(requests, "get", mockreturn)
        with pytest.raises(ZeroResultsException):
            search_mediawiki_page("fake location")

    def test_search_mediawiki_no_response(self, monkeypatch):
        def mockreturn(url, params):
            return MockResponse({}, False)
        monkeypatch.setattr(requests, "get", mockreturn)
        with pytest.raises(NoResponseException):
            search_mediawiki_page(self.location)

    def test_get_media_wiki_extract_ok(self, monkeypatch):
        def mockreturn(url, params):
            return MockResponse({
                "query": {
                    "pages": {
                        "5653202": {
                            "extract" : "My extract"
                        }
                    }
                }
            })
        monkeypatch.setattr(requests, "get", mockreturn)
        assert get_media_wiki_extract("5653202") is not None

    def test_get_media_wiki_extract_zero(self, monkeypatch):
        def mockreturn(url, params):
            return MockResponse({ "query": {} })
        monkeypatch.setattr(requests, "get", mockreturn)
        with pytest.raises(ZeroResultsException):
            get_media_wiki_extract(0)

    def test_get_media_wiki_extract_no_response(self, monkeypatch):
        def mockreturn(url, params):
            return MockResponse({}, False)
        monkeypatch.setattr(requests, "get", mockreturn)
        with pytest.raises(NoResponseException):
            get_media_wiki_extract("5653202")

