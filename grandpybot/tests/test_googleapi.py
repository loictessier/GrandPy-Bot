import pytest
import requests

from grandpybot.utils.googleapi import GoogleApi
from grandpybot.utils.exceptions import ZeroResultsException, NoResponseException


class MockResponse:
    '''Mock for requests.get response call'''
    def __init__(self, result, ok=True):
        self.ok = ok
        self.result = result

    def json(self):
        return self.result

class TestGoogleApi:
    '''Testing the google api methods calls'''

    def setup_method(self):
        self.address_keywords = ["adresse", "openclassrooms", "france"]

    def test_search_ok(self, monkeypatch):
        def mockreturn(url, params):
            return MockResponse({
                    "results":
                    [{
                        "formatted_address":
                            "7 Cité Paradis, 75010 Paris, France"
                    }],
                    "status": "OK"
                })
        monkeypatch.setattr(requests, "get", mockreturn)
        assert GoogleApi.search(self.address_keywords) is not None

    def test_search_zero(self, monkeypatch):
        def mockreturn(url, params):
            return MockResponse({
                    "status": "ZERO_RESULTS"
                })
        monkeypatch.setattr(requests, "get", mockreturn)
        with pytest.raises(ZeroResultsException):
            GoogleApi.search(["adresse", "openclassrooms", "test"])

    def test_search_no_response(self, monkeypatch):
        def mockreturn(url, params):
            return MockResponse({}, False)
        monkeypatch.setattr(requests, "get", mockreturn)
        with pytest.raises(NoResponseException):
            GoogleApi.search(self.address_keywords)