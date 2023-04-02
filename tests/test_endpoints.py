import asyncio
import json
from unittest.mock import AsyncMock, Mock

import aioredis
import pytest
from elasticsearch import AsyncElasticsearch
from fastapi.testclient import TestClient
from mock import patch

from service.searchy import Searchy


@pytest.fixture
def client():
    app = Searchy()
    return TestClient(app.app)


@pytest.mark.skip(name="Should fix mock for async elastic search")
def test_search_endpoint_cache_miss(client, monkeypatch):
    mock_es_instance = AsyncMock(spec=AsyncElasticsearch)
    mock_redis_instance = AsyncMock(spec=aioredis.Redis)

    with patch("elasticsearch.AsyncElasticsearch") as mock_es, \
            patch("aioredis.from_url") as mock_redis:
        mock_es.return_value = mock_es_instance
        future = asyncio.Future()
        future.set_result(mock_redis_instance)
        mock_redis.return_value = future
        expected_result = {"hits": {"hits": [{"_source": {"title": "example title"}}]}}

        mock_es_instance.search.return_value = expected_result
        future = asyncio.Future()
        future.set_result(None)
        mock_redis_instance.set.return_value = future
        future = asyncio.Future()
        future.set_result(None)
        mock_redis_instance.get.return_value = future
        response = client.post("/searchy/api/v1/search", json={"query": "test"})

        assert response.status_code == 200
        assert response.json() == json.dumps(expected_result)


def test_search_endpoint_cache_hit(client, monkeypatch):
    mock_es_instance = AsyncMock(spec=AsyncElasticsearch)
    mock_redis_instance = AsyncMock(spec=aioredis.Redis)
    with patch("elasticsearch.AsyncElasticsearch") as mock_es, \
            patch("aioredis.from_url") as mock_redis:
        mock_es.return_value = mock_es_instance
        future = asyncio.Future()
        future.set_result(mock_redis_instance)
        mock_redis.return_value = future
        expected_result = {"hits": [{"_source": {"title": "example title"}}], "total": 10}

        mock_es_instance.search.return_value = expected_result
        future = asyncio.Future()
        future.set_result(None)
        mock_redis_instance.set.return_value = future
        future = asyncio.Future()
        future.set_result(json.dumps(expected_result).encode())
        mock_redis_instance.get.return_value = future

        response = client.post("/searchy/api/v1/search", json={"query": "test"})
        assert response.status_code == 200
        assert response.json() == expected_result
