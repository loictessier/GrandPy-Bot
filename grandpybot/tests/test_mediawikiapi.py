import pytest
import requests

from grandpybot.utils.mediawikiapi import MediaWikiApi
from grandpybot.utils.exceptions import (ZeroResultsException,
                                         NoResponseException)


class MockResponse:
    '''Mock for requests.get response call'''
    def __init__(self, result, ok=True):
        self.ok = ok
        self.result = result

    def json(self):
        return self.result


class TestMediaWikiApi:
    '''Testing the MediWiki api methods calls'''

    def setup_method(self):
        self.keywords_location = "Cité Paradis"

    def test_search_ok(self, monkeypatch):
        def mockreturn(url, params):
            return MockResponse({
                "query": {
                    "search": [
                        {"pageid": 5653202}
                    ]
                }
            })
        monkeypatch.setattr(requests, "get", mockreturn)
        assert MediaWikiApi.search(self.keywords_location) is not None

    def test_search_zero(self, monkeypatch):
        def mockreturn(url, params):
            return MockResponse({"query": {}})
        monkeypatch.setattr(requests, "get", mockreturn)
        with pytest.raises(ZeroResultsException):
            MediaWikiApi.search("fake location")

    def test_search_no_response(self, monkeypatch):
        def mockreturn(url, params):
            return MockResponse({}, False)
        monkeypatch.setattr(requests, "get", mockreturn)
        with pytest.raises(NoResponseException):
            MediaWikiApi.search(self.keywords_location)

    def test_get_extract_ok(self, monkeypatch):
        def mockreturn(url, params):
            return MockResponse({
                "query": {
                    "pages": {
                        "5653202": {
                            "extract": "My extract"
                        }
                    }
                }
            })
        monkeypatch.setattr(requests, "get", mockreturn)
        assert MediaWikiApi.get_extract("5653202") is not None

    def test_get_extract_zero(self, monkeypatch):
        def mockreturn(url, params):
            return MockResponse({"query": {}})
        monkeypatch.setattr(requests, "get", mockreturn)
        with pytest.raises(ZeroResultsException):
            MediaWikiApi.get_extract(0)

    def test_get_extract_no_response(self, monkeypatch):
        def mockreturn(url, params):
            return MockResponse({}, False)
        monkeypatch.setattr(requests, "get", mockreturn)
        with pytest.raises(NoResponseException):
            MediaWikiApi.get_extract("5653202")
