import pytest
from elasticsearch import Elasticsearch
from fastapi.testclient import TestClient
from unittest.mock import patch

from service.searchy import Searchy


@pytest.fixture
def client():
    app = Searchy()
    return TestClient(app.app)


@pytest.fixture
def mock_es_client():
    with patch.object(Elasticsearch, "__init__", lambda x: None):
        with patch.object(Elasticsearch, "search") as mock_search:
            mock_search.return_value = {
                "hits": {
                    "hits": [
                        {
                            "_source": {
                                "title": "Test Result 1",
                                "description": "This is a test result.",
                            }
                        }
                    ],
                    "total": {"value": 1},
                }
            }
            yield mock_search


def test_search_endpoint(client, mock_es_client):
    response = client.post("/searchy/api/v1/search", json={"query": "test"})
    assert response.status_code == 200
    assert response.json() == {
        "total": 1,
        "hits": [{"title": "Test Result 1", "description": "This is a test result."}],
    }


def test_autocomplete_endpoint(client, mock_es_client):
    response = client.post("/searchy/api/v1/autocomplate", json={"query": "test"})
    assert response.status_code == 200
